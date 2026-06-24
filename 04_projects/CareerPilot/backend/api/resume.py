from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_yaml_config
from core.deps import get_db
from models.database import BaseResume, Job, Profile, ResumeVariant
from resume.ats_scorer import score_ats
from resume.pdf_generator import generate_resume_pdf
from resume.tailorer import tailor_resume

router = APIRouter(prefix="/resume", tags=["resume"])


class TailorRequest(BaseModel):
    profile_id: UUID
    job_id: UUID


class ATSRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/tailor")
async def tailor(data: TailorRequest, db: AsyncSession = Depends(get_db)):
    """Tailor base resume for a specific job using Claude."""
    profile_result = await db.execute(select(Profile).where(Profile.id == data.profile_id))
    profile = profile_result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    resume_result = await db.execute(
        select(BaseResume)
        .where(BaseResume.profile_id == data.profile_id, BaseResume.is_active == True)
        .order_by(BaseResume.version.desc())
        .limit(1)
    )
    base_resume = resume_result.scalar_one_or_none()
    if not base_resume:
        raise HTTPException(status_code=404, detail="No active base resume for this profile")

    job_result = await db.execute(select(Job).where(Job.id == data.job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    tailored = await tailor_resume(
        base_resume.content,
        job.description or "",
        profile.keywords,
        job.title,
        job.company,
    )

    # Score
    resume_text = " ".join([tailored.summary] + tailored.skills)
    ats = score_ats(resume_text, job.description or "")

    # Generate PDF
    from uuid import uuid4
    cfg = get_yaml_config()
    variant_id = uuid4()
    content_dict = tailored.model_dump()
    content_dict["name"] = profile.name
    pdf_path = generate_resume_pdf(content_dict, cfg["resume"]["output_dir"], variant_id)

    # Persist variant
    variant = ResumeVariant(
        id=variant_id,
        profile_id=data.profile_id,
        job_id=data.job_id,
        base_resume_id=base_resume.id,
        tailored_content=content_dict,
        raw_text=resume_text,
        pdf_path=pdf_path,
        ats_score=ats.score,
        keyword_coverage=ats.keyword_coverage,
        injected_keywords=tailored.injected_keywords,
        claude_reasoning=tailored.reasoning,
    )
    db.add(variant)
    await db.flush()

    return {
        "variant_id": str(variant_id),
        "ats_score": ats.score,
        "keyword_coverage": ats.keyword_coverage,
        "matched_keywords": ats.matched_keywords,
        "missing_keywords": ats.missing_keywords,
        "recommendations": ats.recommendations,
        "injected_keywords": tailored.injected_keywords,
        "reasoning": tailored.reasoning,
        "pdf_path": pdf_path,
    }


@router.post("/ats-score")
async def ats_score(data: ATSRequest):
    """Score any resume text against any job description."""
    result = score_ats(data.resume_text, data.job_description)
    return {
        "score": result.score,
        "keyword_coverage": result.keyword_coverage,
        "matched_keywords": result.matched_keywords,
        "missing_keywords": result.missing_keywords,
        "formatting_score": result.formatting_score,
        "length_ok": result.length_ok,
        "recommendations": result.recommendations,
    }


@router.get("/{variant_id}/download")
async def download_resume(variant_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResumeVariant).where(ResumeVariant.id == variant_id))
    variant = result.scalar_one_or_none()
    if not variant or not variant.pdf_path:
        raise HTTPException(status_code=404, detail="Resume PDF not found")
    return FileResponse(
        variant.pdf_path,
        media_type="application/pdf",
        filename=f"resume_{variant_id}.pdf",
    )


@router.get("/variants/{profile_id}")
async def list_variants(profile_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ResumeVariant)
        .where(ResumeVariant.profile_id == profile_id)
        .order_by(ResumeVariant.created_at.desc())
    )
    return result.scalars().all()
