import httpx

from core.config import get_settings

ICONS = {
    "interview_invite": "🎯",
    "offer": "🏆",
    "new_high_match_job": "⚡",
    "rejection": "❌",
    "assessment": "📝",
    "daily_digest": "📊",
}


async def send_telegram(message: str, parse_mode: str = "HTML") -> bool:
    settings = get_settings()
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": settings.telegram_chat_id,
        "text": message,
        "parse_mode": parse_mode,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json=payload)
        return resp.status_code == 200


async def notify_interview(company: str, role: str, summary: str) -> None:
    msg = (
        f"{ICONS['interview_invite']} <b>Interview Invite!</b>\n"
        f"<b>Company:</b> {company}\n"
        f"<b>Role:</b> {role}\n"
        f"<b>Details:</b> {summary}"
    )
    await send_telegram(msg)


async def notify_offer(company: str, role: str, summary: str) -> None:
    msg = (
        f"{ICONS['offer']} <b>JOB OFFER!</b>\n"
        f"<b>Company:</b> {company}\n"
        f"<b>Role:</b> {role}\n"
        f"<b>Details:</b> {summary}"
    )
    await send_telegram(msg)


async def notify_high_match_job(title: str, company: str, score: float, url: str) -> None:
    msg = (
        f"{ICONS['new_high_match_job']} <b>High-Match Job Found!</b>\n"
        f"<b>Role:</b> {title}\n"
        f"<b>Company:</b> {company}\n"
        f"<b>Match Score:</b> {score:.0f}%\n"
        f"<a href='{url}'>View Job</a>"
    )
    await send_telegram(msg)


async def send_daily_digest(
    jobs_found: int,
    jobs_applied: int,
    interviews: int,
    pending_manual: int,
) -> None:
    msg = (
        f"{ICONS['daily_digest']} <b>CareerPilot Daily Report</b>\n\n"
        f"🔍 Jobs discovered: <b>{jobs_found}</b>\n"
        f"✅ Auto-applied: <b>{jobs_applied}</b>\n"
        f"🎯 Interviews: <b>{interviews}</b>\n"
        f"⏳ Manual queue: <b>{pending_manual}</b>"
    )
    await send_telegram(msg)
