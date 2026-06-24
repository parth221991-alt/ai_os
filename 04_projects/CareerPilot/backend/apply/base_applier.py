from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import UUID


class ApplyResult(str, Enum):
    success = "success"
    already_applied = "already_applied"
    failed = "failed"
    limit_reached = "limit_reached"
    captcha = "captcha"
    manual_required = "manual_required"


@dataclass
class ApplyOutcome:
    result: ApplyResult
    application_id: Optional[UUID] = None
    screenshot_path: Optional[str] = None
    error: Optional[str] = None
    notes: str = ""


class BaseApplier(ABC):
    platform: str = ""

    @abstractmethod
    async def apply(
        self,
        job_url: str,
        resume_pdf_path: str,
        cover_letter: str,
        applicant_data: dict,
    ) -> ApplyOutcome:
        ...

    async def _take_screenshot(self, page, screenshots_dir: str, name: str) -> str:
        path = Path(screenshots_dir) / f"{name}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(path), full_page=False)
        return str(path)
