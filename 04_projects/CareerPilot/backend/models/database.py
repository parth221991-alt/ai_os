from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Index,
    Integer, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class JobStatus(str, Enum):
    discovered = "discovered"
    queued = "queued"
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    rejected = "rejected"
    withdrawn = "withdrawn"
    archived = "archived"


class Platform(str, Enum):
    linkedin = "linkedin"
    naukri = "naukri"
    indeed = "indeed"
    company = "company"


class EmailClassification(str, Enum):
    interview_invite = "interview_invite"
    rejection = "rejection"
    assessment = "assessment"
    offer = "offer"
    follow_up = "follow_up"
    general = "general"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)           # "Data Engineer"
    slug = Column(String(100), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    skills = Column(ARRAY(String), default=list)
    keywords = Column(ARRAY(String), default=list)       # ATS keywords for this profile
    experience_years = Column(Integer)
    preferred_locations = Column(ARRAY(String), default=list)
    preferred_salary_min = Column(Integer)
    preferred_salary_max = Column(Integer)
    remote_only = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    base_resumes = relationship("BaseResume", back_populates="profile", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="profile")


class BaseResume(Base):
    __tablename__ = "base_resumes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, default=1)
    content = Column(JSONB, nullable=False)   # structured resume content
    raw_text = Column(Text)                   # plain text for ATS
    file_path = Column(String(500))           # original uploaded file
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("Profile", back_populates="base_resumes")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    platform = Column(String(50), nullable=False)
    platform_job_id = Column(String(200))
    url = Column(Text, nullable=False)
    title = Column(String(300), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200))
    is_remote = Column(Boolean, default=False)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default="INR")
    description = Column(Text)
    requirements = Column(Text)
    posted_at = Column(DateTime(timezone=True))
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    is_easy_apply = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    raw_data = Column(JSONB)

    match_scores = relationship("JobMatchScore", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job")

    __table_args__ = (
        UniqueConstraint("platform", "platform_job_id", name="uq_platform_job"),
        Index("ix_jobs_discovered_at", "discovered_at"),
        Index("ix_jobs_company", "company"),
    )


class JobMatchScore(Base):
    __tablename__ = "job_match_scores"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(PG_UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(PG_UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)
    keyword_matches = Column(ARRAY(String), default=list)
    missing_keywords = Column(ARRAY(String), default=list)
    reasoning = Column(Text)
    scored_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="match_scores")

    __table_args__ = (
        UniqueConstraint("job_id", "profile_id", name="uq_job_profile_score"),
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(PG_UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    profile_id = Column(PG_UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    resume_variant_id = Column(PG_UUID(as_uuid=True), ForeignKey("resume_variants.id"))
    status = Column(String(50), default=JobStatus.applied)
    ats_score = Column(Float)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    last_status_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    screenshot_path = Column(String(500))
    error_log = Column(Text)
    is_auto_applied = Column(Boolean, default=False)

    job = relationship("Job", back_populates="applications")
    profile = relationship("Profile", back_populates="applications")
    resume_variant = relationship("ResumeVariant", back_populates="application")
    email_threads = relationship("EmailThread", back_populates="application")

    __table_args__ = (
        UniqueConstraint("job_id", "profile_id", name="uq_application"),
        Index("ix_applications_status", "status"),
    )


class ResumeVariant(Base):
    __tablename__ = "resume_variants"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(PG_UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    job_id = Column(PG_UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    base_resume_id = Column(PG_UUID(as_uuid=True), ForeignKey("base_resumes.id"), nullable=False)
    tailored_content = Column(JSONB, nullable=False)
    raw_text = Column(Text)
    pdf_path = Column(String(500))
    ats_score = Column(Float)
    keyword_coverage = Column(Float)
    injected_keywords = Column(ARRAY(String), default=list)
    claude_reasoning = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="resume_variant", uselist=False)


class EmailThread(Base):
    __tablename__ = "email_threads"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(PG_UUID(as_uuid=True), ForeignKey("applications.id"))
    gmail_thread_id = Column(String(200), unique=True, nullable=False)
    gmail_message_id = Column(String(200))
    subject = Column(String(500))
    sender = Column(String(300))
    snippet = Column(Text)
    classification = Column(String(50), default=EmailClassification.general)
    confidence = Column(Float)
    received_at = Column(DateTime(timezone=True))
    is_read = Column(Boolean, default=False)
    is_notified = Column(Boolean, default=False)
    raw_content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="email_threads")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(50), nullable=False)
    title = Column(String(300), nullable=False)
    body = Column(Text)
    extra = Column(JSONB, default=dict)
    is_read = Column(Boolean, default=False)
    telegram_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApplyLog(Base):
    __tablename__ = "apply_logs"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    platform = Column(String(50), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    count = Column(Integer, default=0)

    __table_args__ = (
        Index("ix_apply_logs_platform_date", "platform", "date"),
    )


# ── DB engine factory ────────────────────────────────────────────────────────

_engine = None
_session_factory = None


def get_engine(database_url: str):
    global _engine
    if _engine is None:
        _engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
    return _engine


def get_session_factory(database_url: str) -> async_sessionmaker:
    global _session_factory
    if _session_factory is None:
        engine = get_engine(database_url)
        _session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return _session_factory
