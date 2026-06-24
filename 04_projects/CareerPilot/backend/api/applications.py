from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from models.database import Application, Job, JobStatus, Profile, ResumeVariant

router = APIRouter(prefix="/applications", tags=["applications"])


class ApplicationCreate(BaseModel):
    job_id: UUID
    profile_id: UUID
    notes: str = ""


class StatusUpdate(BaseModel):
    status: str
    notes: str | None = None


@router.get("/")
async def list_applications(
    status: str | None = None,
    profile_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Application, Job)
        .join(Job, Application.job_id == Job.id)
        .order_by(Application.applied_at.desc())
    )
    if status:
        query = query.where(Application.status == status)
    if profile_id:
        query = query.where(Application.profile_id == profile_id)

    result = await db.execute(query)
    rows = result.all()

    output = []
    for app, job in rows:
        d = {c.name: getattr(app, c.name) for c in app.__table__.columns}
        d["job_title"] = job.title
        d["company"] = job.company
        d["job_url"] = job.url
        d["platform"] = job.platform
        output.append(d)
    return output


@router.post("/", status_code=201)
async def create_manual_application(
    data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Manually mark a job as applied (for jobs applied outside the system)."""
    existing = await db.execute(
        select(Application).where(
            Application.job_id == data.job_id,
            Application.profile_id == data.profile_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Already applied to this job")

    app = Application(
        job_id=data.job_id,
        profile_id=data.profile_id,
        status=JobStatus.applied,
        notes=data.notes,
        is_auto_applied=False,
    )
    db.add(app)
    await db.flush()
    return app


@router.patch("/{application_id}/status")
async def update_status(
    application_id: UUID,
    data: StatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Application).where(Application.id == application_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = data.status
    if data.notes:
        app.notes = data.notes
    return app


@router.get("/pipeline")
async def get_pipeline(db: AsyncSession = Depends(get_db)):
    """Kanban-style pipeline counts."""
    result = await db.execute(select(Application))
    apps = result.scalars().all()

    pipeline: dict[str, int] = {}
    for app in apps:
        pipeline[app.status] = pipeline.get(app.status, 0) + 1
    return pipeline


@router.post("/{application_id}/apply", status_code=202)
async def trigger_auto_apply(
    application_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Re-attempt auto-apply for a manual_required application."""
    result = await db.execute(select(Application).where(Application.id == application_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    background_tasks.add_task(_retry_apply, application_id)
    return {"message": "Apply retry queued"}


async def _retry_apply(application_id: UUID):
    from scheduler.jobs import run_auto_apply
    # Simplified retry — a full retry would target this specific application
    await run_auto_apply()
