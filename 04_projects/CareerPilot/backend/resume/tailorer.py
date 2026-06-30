import json
from typing import Any

import anthropic
from pydantic import BaseModel

from core.config import get_settings, get_yaml_config


class TailoredResume(BaseModel):
    summary: str
    skills: list[str]
    experience: list[dict[str, Any]]
    education: list[dict[str, Any]]
    certifications: list[dict[str, Any]]
    injected_keywords: list[str]
    reasoning: str


SYSTEM_PROMPT = """You are a professional resume writer specializing in technical roles in data engineering,
data architecture, and AI/ML. Your job is to tailor a candidate's base resume to match a specific job description
while maximizing ATS compatibility.

Rules:
- Never fabricate experience or skills the candidate does not have
- Reorder and reframe existing content to match the job's priority keywords
- Inject missing keywords from the JD only when truthfully applicable
- Keep total length under 2 pages (max 600 words for experience sections)
- Preserve all dates, companies, and factual details exactly
- Output valid JSON matching the TailoredResume schema"""


async def tailor_resume(
    base_resume: dict[str, Any],
    job_description: str,
    profile_keywords: list[str],
    job_title: str,
    company: str,
) -> TailoredResume:
    settings = get_settings()
    cfg = get_yaml_config()

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    jd_section = job_description.strip() if job_description and len(job_description) > 50 else (
        f"[Full description unavailable — tailor based on job title: {job_title} at {company}. "
        f"Prioritize these profile keywords: {', '.join(profile_keywords[:15])}]"
    )

    user_content = f"""
Job Title: {job_title}
Company: {company}

Job Description:
{jd_section}

Profile Keywords to Prioritize:
{', '.join(profile_keywords)}

Base Resume:
{json.dumps(base_resume, indent=2)}

Tailor this resume for the job above. Return ONLY valid JSON matching the TailoredResume schema.
Schema: {json.dumps(TailoredResume.model_json_schema(), indent=2)}
"""

    message = await client.messages.create(
        model=cfg["ai"]["reasoning_model"],
        max_tokens=cfg["ai"]["max_tokens"],
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)
    return TailoredResume(**data)
