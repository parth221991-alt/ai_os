"""
Company career page applier — best-effort form detection.
Handles generic HTML forms on company websites. Since every company's
ATS is different (Workday, Greenhouse, Lever, Taleo, etc.), this
attempts common patterns and falls back to manual_required when it can't proceed.
"""
import asyncio
from pathlib import Path
from uuid import uuid4

from playwright.async_api import Page, async_playwright

from apply.base_applier import ApplyOutcome, ApplyResult, BaseApplier
from core.config import get_yaml_config

# Known ATS patterns
ATS_PATTERNS = {
    "greenhouse": {
        "submit": "#submit_app",
        "resume": "input[type='file']",
        "first_name": "#first_name",
        "last_name": "#last_name",
        "email": "#email",
        "phone": "#phone",
        "cover_letter": "#cover_letter",
    },
    "lever": {
        "submit": "button[type='submit']",
        "resume": ".lever-upload input[type='file']",
        "first_name": "input[name='name']",
        "email": "input[name='email']",
        "phone": "input[name='phone']",
        "cover_letter": "textarea[name='comments']",
    },
    "workday": {
        # Workday requires extensive JS interaction — flag as manual
        "manual": True,
    },
    "taleo": {
        "manual": True,
    },
}


def _detect_ats(url: str) -> str | None:
    url_lower = url.lower()
    for ats in ["greenhouse", "lever", "workday", "taleo"]:
        if ats in url_lower:
            return ats
    return None


class CompanyApplier(BaseApplier):
    platform = "company"

    async def apply(
        self,
        job_url: str,
        resume_pdf_path: str,
        cover_letter: str,
        applicant_data: dict,
    ) -> ApplyOutcome:
        cfg = get_yaml_config()
        shot_id = str(uuid4())[:8]
        ats = _detect_ats(job_url)

        # Known-manual ATS systems
        if ats in ("workday", "taleo"):
            return ApplyOutcome(
                result=ApplyResult.manual_required,
                notes=f"{ats.title()} ATS detected — requires manual application",
            )

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=cfg["scraper"]["headless"])
            context = await browser.new_context(user_agent=cfg["scraper"]["user_agent"])
            page = await context.new_page()

            try:
                outcome = await self._generic_apply(
                    page, job_url, resume_pdf_path, cover_letter,
                    applicant_data, shot_id, ats, cfg
                )
            except Exception as e:
                screenshot = await self._take_screenshot(page, "screenshots", f"co_error_{shot_id}")
                outcome = ApplyOutcome(
                    result=ApplyResult.manual_required,
                    screenshot_path=screenshot,
                    error=str(e),
                    notes="Company apply failed — add to manual queue",
                )
            finally:
                await browser.close()

        return outcome

    async def _generic_apply(
        self,
        page: Page,
        job_url: str,
        resume_path: str,
        cover_letter: str,
        applicant_data: dict,
        shot_id: str,
        ats: str | None,
        cfg: dict,
    ) -> ApplyOutcome:
        await page.goto(job_url, wait_until="networkidle")
        await asyncio.sleep(2)

        selectors = ATS_PATTERNS.get(ats, {}) if ats else {}

        # Fill name
        first = applicant_data.get("first_name", "")
        last = applicant_data.get("last_name", "")
        email = applicant_data.get("email", "")
        phone = applicant_data.get("phone", "")

        for sel_key, value in [
            ("first_name", first), ("last_name", last),
            ("email", email), ("phone", phone),
        ]:
            sel = selectors.get(sel_key) or f"input[name*='{sel_key}'], input[id*='{sel_key}']"
            try:
                el = await page.query_selector(sel)
                if el and value:
                    await el.fill(value)
            except Exception:
                pass

        # Upload resume
        resume_sel = selectors.get("resume", "input[type='file']")
        try:
            file_input = await page.query_selector(resume_sel)
            if file_input:
                await file_input.set_input_files(resume_path)
                await asyncio.sleep(1)
        except Exception:
            pass

        # Cover letter
        cl_sel = selectors.get("cover_letter", "textarea")
        try:
            cl_el = await page.query_selector(cl_sel)
            if cl_el:
                await cl_el.fill(cover_letter[:3000])
        except Exception:
            pass

        # Submit
        submit_sel = selectors.get("submit", "button[type='submit']")
        try:
            submit_btn = await page.query_selector(submit_sel)
            if submit_btn:
                screenshot_pre = await self._take_screenshot(page, "screenshots", f"co_pre_{shot_id}")
                await submit_btn.click()
                await asyncio.sleep(2)
                screenshot = await self._take_screenshot(page, "screenshots", f"co_confirm_{shot_id}")
                return ApplyOutcome(result=ApplyResult.success, screenshot_path=screenshot)
        except Exception:
            pass

        screenshot = await self._take_screenshot(page, "screenshots", f"co_manual_{shot_id}")
        return ApplyOutcome(
            result=ApplyResult.manual_required,
            screenshot_path=screenshot,
            notes="Could not find submit button — added to manual queue",
        )
