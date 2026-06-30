from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from models.database import Job, JobMatchScore
from scheduler.jobs import run_job_discovery

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
async def list_jobs(
    platform: str | None = Query(None),
    min_score: float = Query(0),
    profile_id: UUID | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Job).where(Job.is_active == True)
    if platform:
        query = query.where(Job.platform == platform)
    query = query.order_by(Job.discovered_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = result.scalars().all()

    job_ids = [j.id for j in jobs]

    if profile_id:
        # Specific profile: return that profile's score + matched keywords
        scores_result = await db.execute(
            select(JobMatchScore).where(
                JobMatchScore.job_id.in_(job_ids),
                JobMatchScore.profile_id == profile_id,
            )
        )
        score_map: dict = {s.job_id: s for s in scores_result.scalars().all()}
    else:
        # All profiles: attach best (max) score across all profiles so column is never blank
        best_result = await db.execute(
            select(JobMatchScore.job_id, func.max(JobMatchScore.score).label("best_score"))
            .where(JobMatchScore.job_id.in_(job_ids))
            .group_by(JobMatchScore.job_id)
        )
        score_map = {row.job_id: row.best_score for row in best_result.all()}

    enriched = []
    for job in jobs:
        job_dict = {c.name: getattr(job, c.name) for c in job.__table__.columns}
        if profile_id:
            score_obj = score_map.get(job.id)
            job_dict["match_score"] = score_obj.score if score_obj else None
            job_dict["matched_keywords"] = score_obj.keyword_matches if score_obj else []
        else:
            best = score_map.get(job.id)
            job_dict["match_score"] = best if best is not None else None
            job_dict["matched_keywords"] = []
        if min_score and (job_dict["match_score"] or 0) < min_score:
            continue
        enriched.append(job_dict)

    return enriched


@router.get("/{job_id}")
async def get_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    return result.scalar_one_or_none()


@router.post("/discover", status_code=202)
async def trigger_discovery(background_tasks: BackgroundTasks):
    """Manually trigger job discovery (runs as background task)."""
    background_tasks.add_task(run_job_discovery)
    return {"message": "Job discovery started"}


@router.get("/{job_id}/scores")
async def get_job_scores(job_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(JobMatchScore).where(JobMatchScore.job_id == job_id)
    )
    return result.scalars().all()
