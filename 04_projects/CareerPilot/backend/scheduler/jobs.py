"""
APScheduler tasks for daily job discovery, auto-apply, and email polling.
All tasks run async and respect daily apply limits from settings.yaml.
"""
import asyncio
import logging
from datetime import date, datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings, get_yaml_config
from email_monitor.classifier import classify_email
from email_monitor.gmail_client import fetch_recent_career_emails, mark_as_read
from models.database import (
    Application, ApplyLog, EmailThread, Job, JobMatchScore,
    Notification, Profile, ResumeVariant, get_session_factory
)
from notifications.telegram import (
    notify_high_match_job, notify_interview, notify_offer, send_daily_digest
)
from resume.ats_scorer import score_ats
from resume.tailorer import tailor_resume

log = logging.getLogger("careerpilot.scheduler")


async def _get_daily_apply_count(session: AsyncSession, platform: str) -> int:
    today = date.today()
    result = await session.execute(
        select(func.sum(ApplyLog.count)).where(
            ApplyLog.platform == platform,
            func.date(ApplyLog.date) == today,
        )
    )
    return result.scalar() or 0


async def _increment_apply_log(session: AsyncSession, platform: str) -> None:
    today = date.today()
    result = await session.execute(
        select(ApplyLog).where(
            ApplyLog.platform == platform,
            func.date(ApplyLog.date) == today,
        )
    )
    log_entry = result.scalar_one_or_none()
    if log_entry:
        log_entry.count += 1
    else:
        session.add(ApplyLog(platform=platform, count=1))
    await session.flush()


async def run_job_discovery():
    """Scrape all platforms, deduplicate, score against all profiles."""
    from scrapers.linkedin import LinkedInScraper
    from scrapers.naukri import NaukriScraper
    from scrapers.indeed import IndeedScraper

    settings = get_settings()
    cfg = get_yaml_config()
    factory = get_session_factory(settings.database_url)

    async with factory() as session:
        # Load active profiles
        result = await session.execute(select(Profile).where(Profile.is_active == True))
        profiles = result.scalars().all()

        if not profiles:
            log.warning("No active profiles found — skipping discovery")
            return

        # Build search queries from all profiles
        queries: list[str] = []
        for p in profiles:
            queries.append(p.title)
            queries.extend(p.keywords[:3])  # top 3 keywords per profile
        queries = list(set(queries))

        max_per_platform = cfg["scraper"]["max_jobs_per_platform_per_run"]
        lookback = cfg["scraper"]["lookback_days"]

        scrapers = [LinkedInScraper(), NaukriScraper(), IndeedScraper()]
        all_scraped = []
        for scraper in scrapers:
            try:
                jobs = await scraper.scrape(queries, max_jobs=max_per_platform, lookback_days=lookback)
                all_scraped.extend(jobs)
                log.info(f"{scraper.platform}: scraped {len(jobs)} jobs")
            except Exception as e:
                log.error(f"{scraper.platform} scraper failed: {e}")

        # Upsert jobs + score
        new_jobs = 0
        for scraped in all_scraped:
            # Check duplicate
            exists = await session.execute(
                select(Job).where(
                    Job.platform == scraped.platform,
                    Job.platform_job_id == scraped.platform_job_id,
                )
            )
            job = exists.scalar_one_or_none()
            if not job:
                job = Job(
                    platform=scraped.platform,
                    platform_job_id=scraped.platform_job_id,
                    url=scraped.url,
                    title=scraped.title,
                    company=scraped.company,
                    location=scraped.location,
                    description=scraped.description,
                    requirements=scraped.requirements,
                    is_remote=scraped.is_remote,
                    is_easy_apply=scraped.is_easy_apply,
                    posted_at=scraped.posted_at,
                    raw_data=scraped.raw_data,
                )
                session.add(job)
                await session.flush()
                new_jobs += 1

            # Score against each profile
            for profile in profiles:
                score_exists = await session.execute(
                    select(JobMatchScore).where(
                        JobMatchScore.job_id == job.id,
                        JobMatchScore.profile_id == profile.id,
                    )
                )
                if not score_exists.scalar_one_or_none():
                    jd_text = f"{scraped.title} {scraped.description}"
                    resume_text = " ".join(profile.keywords + profile.skills)
                    ats = score_ats(resume_text, jd_text)

                    match = JobMatchScore(
                        job_id=job.id,
                        profile_id=profile.id,
                        score=ats.score,
                        keyword_matches=ats.matched_keywords,
                        missing_keywords=ats.missing_keywords,
                    )
                    session.add(match)

                    # Notify on high match
                    if ats.score >= 80:
                        await notify_high_match_job(
                            scraped.title, scraped.company, ats.score, scraped.url
                        )

        await session.commit()
        log.info(f"Discovery complete: {new_jobs} new jobs added")


async def run_auto_apply():
    """Apply to queued high-score jobs that are easy-apply eligible."""
    from apply.linkedin_applier import LinkedInApplier
    from apply.naukri_applier import NaukriApplier
    from apply.indeed_applier import IndeedApplier
    from apply.company_applier import CompanyApplier
    from apply.base_applier import ApplyResult

    settings = get_settings()
    cfg = get_yaml_config()
    limits = cfg["apply_limits"]
    factory = get_session_factory(settings.database_url)

    appliers = {
        "linkedin": LinkedInApplier(),
        "naukri": NaukriApplier(),
        "indeed": IndeedApplier(),
        "company": CompanyApplier(),
    }

    async with factory() as session:
        profiles_result = await session.execute(select(Profile).where(Profile.is_active == True))
        profiles = profiles_result.scalars().all()

        for profile in profiles:
            # Get high-score undiscovered jobs eligible for auto-apply
            scores_result = await session.execute(
                select(JobMatchScore, Job)
                .join(Job, JobMatchScore.job_id == Job.id)
                .where(
                    JobMatchScore.profile_id == profile.id,
                    JobMatchScore.score >= 65,
                    Job.is_active == True,
                )
                .order_by(JobMatchScore.score.desc())
                .limit(50)
            )
            candidates = scores_result.all()

            for score_row, job in candidates:
                # Skip if already applied
                existing = await session.execute(
                    select(Application).where(
                        Application.job_id == job.id,
                        Application.profile_id == profile.id,
                    )
                )
                if existing.scalar_one_or_none():
                    continue

                platform = job.platform
                daily_limit = limits.get(platform, {}).get("daily_max", 10)
                current_count = await _get_daily_apply_count(session, platform)
                if current_count >= daily_limit:
                    log.info(f"Daily limit reached for {platform}")
                    break

                # Load best active base resume for profile
                from models.database import BaseResume
                base_result = await session.execute(
                    select(BaseResume).where(
                        BaseResume.profile_id == profile.id,
                        BaseResume.is_active == True,
                    ).order_by(BaseResume.version.desc()).limit(1)
                )
                base_resume = base_result.scalar_one_or_none()
                if not base_resume:
                    continue

                # Tailor resume with Claude
                try:
                    tailored = await tailor_resume(
                        base_resume.content,
                        job.description or "",
                        profile.keywords,
                        job.title,
                        job.company,
                    )
                except Exception as e:
                    log.error(f"Resume tailoring failed for {job.id}: {e}")
                    continue

                # Score the tailored resume
                resume_text = " ".join(
                    [tailored.summary] + tailored.skills +
                    [b for exp in tailored.experience for b in exp.get("bullets", [])]
                )
                ats_result = score_ats(resume_text, job.description or "")

                # Generate PDF
                from uuid import uuid4
                from resume.pdf_generator import generate_resume_pdf

                variant_id = uuid4()
                content_dict = tailored.model_dump()
                content_dict["name"] = profile.name
                pdf_path = generate_resume_pdf(
                    content_dict,
                    cfg["resume"]["output_dir"],
                    variant_id,
                )

                # Save variant
                variant = ResumeVariant(
                    id=variant_id,
                    profile_id=profile.id,
                    job_id=job.id,
                    base_resume_id=base_resume.id,
                    tailored_content=content_dict,
                    raw_text=resume_text,
                    pdf_path=pdf_path,
                    ats_score=ats_result.score,
                    keyword_coverage=ats_result.keyword_coverage,
                    injected_keywords=tailored.injected_keywords,
                    claude_reasoning=tailored.reasoning,
                )
                session.add(variant)
                await session.flush()

                # Attempt apply
                applicant_data = {
                    "first_name": profile.name.split()[0] if profile.name else "",
                    "last_name": profile.name.split()[-1] if profile.name else "",
                    "email": settings.gmail_email if hasattr(settings, "gmail_email") else "",
                    "phone": "",
                }

                applier = appliers.get(platform)
                if not applier:
                    continue

                delay = limits.get(platform, {}).get("delay_between_applications_sec", 45)
                await asyncio.sleep(delay)

                outcome = await applier.apply(
                    job_url=job.url,
                    resume_pdf_path=pdf_path,
                    cover_letter=f"Please find my tailored resume attached for the {job.title} role at {job.company}.",
                    applicant_data=applicant_data,
                )

                # Record application
                from models.database import JobStatus
                status = JobStatus.applied if outcome.result == ApplyResult.success else "manual_required"
                app = Application(
                    job_id=job.id,
                    profile_id=profile.id,
                    resume_variant_id=variant.id,
                    status=status,
                    ats_score=ats_result.score,
                    screenshot_path=outcome.screenshot_path,
                    error_log=outcome.error,
                    is_auto_applied=outcome.result == ApplyResult.success,
                    notes=outcome.notes,
                )
                session.add(app)
                await _increment_apply_log(session, platform)
                await session.flush()

                log.info(f"Applied to {job.title} @ {job.company}: {outcome.result}")

        await session.commit()


async def run_email_monitor():
    """Fetch unread career emails, classify, link to applications, notify."""
    settings = get_settings()
    factory = get_session_factory(settings.database_url)

    try:
        emails = fetch_recent_career_emails(max_results=30)
    except Exception as e:
        log.error(f"Gmail fetch failed: {e}")
        return

    async with factory() as session:
        for email in emails:
            thread_id = email["gmail_thread_id"]

            # Skip already processed threads
            existing = await session.execute(
                select(EmailThread).where(EmailThread.gmail_thread_id == thread_id)
            )
            if existing.scalar_one_or_none():
                continue

            # Classify
            try:
                classification = await classify_email(
                    email["subject"], email["sender"], email["body"]
                )
            except Exception as e:
                log.error(f"Classification failed: {e}")
                continue

            # Try to link to an application by company name
            linked_app_id = None
            if classification.company:
                app_result = await session.execute(
                    select(Application)
                    .join(Job, Application.job_id == Job.id)
                    .where(Job.company.ilike(f"%{classification.company}%"))
                    .order_by(Application.applied_at.desc())
                    .limit(1)
                )
                linked_app = app_result.scalar_one_or_none()
                if linked_app:
                    linked_app_id = linked_app.id

                    # Update application status
                    if classification.classification == "interview_invite":
                        linked_app.status = "interviewing"
                    elif classification.classification == "offer":
                        linked_app.status = "offer"
                    elif classification.classification == "rejection":
                        linked_app.status = "rejected"

            thread = EmailThread(
                application_id=linked_app_id,
                gmail_thread_id=thread_id,
                gmail_message_id=email["gmail_message_id"],
                subject=email["subject"],
                sender=email["sender"],
                snippet=email["snippet"],
                classification=classification.classification,
                confidence=classification.confidence,
                raw_content=email["body"][:5000],
            )
            session.add(thread)

            # Notifications
            if classification.classification == "interview_invite":
                await notify_interview(classification.company, classification.role, classification.summary)
            elif classification.classification == "offer":
                await notify_offer(classification.company, classification.role, classification.summary)

            # In-app notification
            if classification.action_required:
                session.add(Notification(
                    type=classification.classification,
                    title=f"{classification.company}: {classification.classification.replace('_', ' ').title()}",
                    body=classification.summary,
                    extra={"email_thread_id": str(thread_id)},
                ))

            mark_as_read(email["gmail_message_id"])

        await session.commit()


async def run_daily_digest():
    """Send a Telegram summary of the day's activity."""
    settings = get_settings()
    factory = get_session_factory(settings.database_url)
    today = date.today()

    async with factory() as session:
        jobs_found = (await session.execute(
            select(func.count(Job.id)).where(func.date(Job.discovered_at) == today)
        )).scalar() or 0

        jobs_applied = (await session.execute(
            select(func.count(Application.id)).where(func.date(Application.applied_at) == today)
        )).scalar() or 0

        interviews = (await session.execute(
            select(func.count(Application.id)).where(
                Application.status == "interviewing",
                func.date(Application.last_status_at) == today,
            )
        )).scalar() or 0

        manual_queue = (await session.execute(
            select(func.count(Application.id)).where(Application.status == "manual_required")
        )).scalar() or 0

    await send_daily_digest(jobs_found, jobs_applied, interviews, manual_queue)


def create_scheduler(cfg: dict) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=cfg["scheduler"]["timezone"])

    scheduler.add_job(
        run_job_discovery,
        CronTrigger.from_crontab(cfg["scheduler"]["job_discovery_cron"]),
        id="job_discovery",
        replace_existing=True,
    )

    scheduler.add_job(
        run_auto_apply,
        CronTrigger.from_crontab(cfg["scheduler"]["job_discovery_cron"]),
        id="auto_apply",
        replace_existing=True,
    )

    scheduler.add_job(
        run_email_monitor,
        "interval",
        seconds=cfg["scheduler"]["email_poll_interval"],
        id="email_monitor",
        replace_existing=True,
    )

    # Daily digest at 6 PM IST
    scheduler.add_job(
        run_daily_digest,
        CronTrigger(hour=18, minute=0, timezone=cfg["scheduler"]["timezone"]),
        id="daily_digest",
        replace_existing=True,
    )

    return scheduler
