from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from models.database import EmailThread, Notification
from scheduler.jobs import run_email_monitor

router = APIRouter(prefix="/email", tags=["email"])


@router.get("/threads")
async def list_threads(
    classification: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(EmailThread).order_by(EmailThread.received_at.desc()).limit(100)
    if classification:
        query = query.where(EmailThread.classification == classification)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/threads/{thread_id}")
async def get_thread(thread_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EmailThread).where(EmailThread.gmail_thread_id == thread_id)
    )
    return result.scalar_one_or_none()


@router.post("/sync", status_code=202)
async def sync_emails(background_tasks: BackgroundTasks):
    """Manually trigger email sync."""
    background_tasks.add_task(run_email_monitor)
    return {"message": "Email sync started"}


@router.get("/notifications")
async def list_notifications(
    unread_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    query = select(Notification).order_by(Notification.created_at.desc()).limit(50)
    if unread_only:
        query = query.where(Notification.is_read == False)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, db: AsyncSession = Depends(get_db)):
    from uuid import UUID
    result = await db.execute(
        select(Notification).where(Notification.id == UUID(notification_id))
    )
    notif = result.scalar_one_or_none()
    if notif:
        notif.is_read = True
    return {"ok": True}
