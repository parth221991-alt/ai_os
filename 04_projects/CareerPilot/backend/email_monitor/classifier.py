import anthropic
from pydantic import BaseModel

from core.config import get_settings, get_yaml_config


class EmailClassification(BaseModel):
    classification: str   # interview_invite | rejection | assessment | offer | follow_up | general
    confidence: float     # 0.0–1.0
    company: str
    role: str
    action_required: bool
    summary: str


SYSTEM_PROMPT = """You are an email classifier for a job seeker's career assistant.
Classify each email into exactly one category and extract key information.

Categories:
- interview_invite: Recruiter or hiring manager scheduling an interview
- rejection: Application declined or position filled
- assessment: Technical test, coding challenge, or assignment
- offer: Job offer or offer letter
- follow_up: Status update, "still reviewing", "next steps" emails
- general: Anything else career-related

Always respond with valid JSON matching the EmailClassification schema."""


async def classify_email(
    subject: str,
    sender: str,
    body: str,
) -> EmailClassification:
    settings = get_settings()
    cfg = get_yaml_config()

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_content = f"""
Subject: {subject}
From: {sender}
Body (first 1000 chars): {body[:1000]}

Classify this email. Return JSON:
{{"classification": "...", "confidence": 0.0-1.0, "company": "...", "role": "...", "action_required": true/false, "summary": "one sentence"}}
"""

    message = await client.messages.create(
        model=cfg["ai"]["throughput_model"],
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )

    import json
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw.strip())
    return EmailClassification(**data)
