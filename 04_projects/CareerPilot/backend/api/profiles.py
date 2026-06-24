from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from models.database import BaseResume, Profile

router = APIRouter(prefix="/profiles", tags=["profiles"])


class ProfileCreate(BaseModel):
    name: str
    slug: str
    title: str
    summary: str = ""
    skills: list[str] = []
    keywords: list[str] = []
    experience_years: int = 0
    preferred_locations: list[str] = []
    preferred_salary_min: int | None = None
    preferred_salary_max: int | None = None
    remote_only: bool = False


class ProfileUpdate(BaseModel):
    name: str | None = None
    title: str | None = None
    summary: str | None = None
    skills: list[str] | None = None
    keywords: list[str] | None = None
    experience_years: int | None = None
    preferred_locations: list[str] | None = None
    preferred_salary_min: int | None = None
    preferred_salary_max: int | None = None
    remote_only: bool | None = None
    is_active: bool | None = None


class BaseResumeCreate(BaseModel):
    content: dict
    raw_text: str = ""


@router.get("/")
async def list_profiles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).order_by(Profile.created_at))
    return result.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    profile = Profile(**data.model_dump())
    db.add(profile)
    await db.flush()
    return profile


@router.get("/{profile_id}")
async def get_profile(profile_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/{profile_id}")
async def update_profile(
    profile_id: UUID, data: ProfileUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(profile, field, value)
    return profile


@router.post("/{profile_id}/resumes", status_code=status.HTTP_201_CREATED)
async def upload_base_resume(
    profile_id: UUID, data: BaseResumeCreate, db: AsyncSession = Depends(get_db)
):
    # Deactivate previous versions
    result = await db.execute(
        select(BaseResume).where(BaseResume.profile_id == profile_id, BaseResume.is_active == True)
    )
    for old in result.scalars().all():
        old.is_active = False

    # Get next version number
    version_result = await db.execute(
        select(BaseResume).where(BaseResume.profile_id == profile_id).order_by(BaseResume.version.desc()).limit(1)
    )
    latest = version_result.scalar_one_or_none()
    version = (latest.version + 1) if latest else 1

    resume = BaseResume(
        profile_id=profile_id,
        content=data.content,
        raw_text=data.raw_text,
        version=version,
        is_active=True,
    )
    db.add(resume)
    await db.flush()
    return resume


@router.get("/{profile_id}/resumes")
async def list_resumes(profile_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BaseResume)
        .where(BaseResume.profile_id == profile_id)
        .order_by(BaseResume.version.desc())
    )
    return result.scalars().all()
