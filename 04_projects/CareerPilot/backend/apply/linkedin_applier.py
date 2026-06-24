import asyncio
from datetime import date
from pathlib import Path
from uuid import uuid4

from playwright.async_api import Page, async_playwright

from apply.base_applier import ApplyOutcome, ApplyResult, BaseApplier
from core.config import get_settings, get_yaml_config


class LinkedInApplier(BaseApplier):
    platform = "linkedin"

    async def apply(
        self,
        job_url: str,
        resume_pdf_path: str,
        cover_letter: str,
        applicant_data: dict,
    ) -> ApplyOutcome:
        cfg = get_yaml_config()
        settings = get_settings()
        shot_id = str(uuid4())[:8]

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=cfg["scraper"]["headless"])
            context = await browser.new_context(user_agent=cfg["scraper"]["user_agent"])
            page = await context.new_page()

            try:
                await self._login(page, settings.linkedin_email, settings.linkedin_password)
                outcome = await self._easy_apply(
                    page, job_url, resume_pdf_path, cover_letter, applicant_data, shot_id, cfg
                )
            except Exception as e:
                screenshot = await self._take_screenshot(page, "screenshots", f"li_error_{shot_id}")
                outcome = ApplyOutcome(
                    result=ApplyResult.failed,
                    screenshot_path=screenshot,
                    error=str(e),
                )
            finally:
                await browser.close()

        return outcome

    async def _login(self, page: Page, email: str, password: str) -> None:
        await page.goto("https://www.linkedin.com/login", wait_until="networkidle")
        await page.fill("#username", email)
        await page.fill("#password", password)
        await page.click('[type="submit"]')
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

    async def _easy_apply(
        self,
        page: Page,
        job_url: str,
        resume_path: str,
        cover_letter: str,
        applicant_data: dict,
        shot_id: str,
        cfg: dict,
    ) -> ApplyOutcome:
        await page.goto(job_url, wait_until="networkidle")
        await asyncio.sleep(2)

        # Check if already applied
        applied_el = await page.query_selector(".jobs-apply-button--applied")
        if applied_el:
            return ApplyOutcome(result=ApplyResult.already_applied)

        # Click Easy Apply button
        apply_btn = await page.query_selector(".jobs-apply-button--top-card")
        if not apply_btn:
            return ApplyOutcome(result=ApplyResult.manual_required, notes="No Easy Apply button")

        btn_text = (await apply_btn.inner_text()).lower()
        if "easy apply" not in btn_text:
            return ApplyOutcome(result=ApplyResult.manual_required, notes="Not Easy Apply")

        await apply_btn.click()
        await asyncio.sleep(2)

        # Walk through the Easy Apply modal steps
        max_steps = 10
        for step in range(max_steps):
            modal = await page.query_selector(".jobs-easy-apply-modal")
            if not modal:
                break

            # Upload resume if prompted
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(resume_path)
                await asyncio.sleep(1)

            # Fill phone if needed
            phone_input = await page.query_selector("input[id*='phoneNumber']")
            if phone_input:
                current = await phone_input.input_value()
                if not current:
                    await phone_input.fill(applicant_data.get("phone", ""))

            # Cover letter textarea
            cover_el = await page.query_selector("textarea[id*='coverLetter']")
            if cover_el:
                await cover_el.fill(cover_letter[:2000])

            # Handle yes/no radio questions (default to "Yes" for work authorization etc.)
            radios = await page.query_selector_all("input[type='radio']")
            for radio in radios:
                label = await radio.get_attribute("aria-label") or ""
                val = await radio.get_attribute("value") or ""
                if val.lower() in ("yes", "true") and "authorized" in label.lower():
                    await radio.click()

            # Check for "Next" or "Submit" button
            next_btn = await page.query_selector("button[aria-label='Continue to next step']")
            submit_btn = await page.query_selector("button[aria-label='Submit application']")
            review_btn = await page.query_selector("button[aria-label='Review your application']")

            if submit_btn:
                screenshot = await self._take_screenshot(page, "screenshots", f"li_pre_submit_{shot_id}")
                await submit_btn.click()
                await asyncio.sleep(2)
                confirm = await self._take_screenshot(page, "screenshots", f"li_confirm_{shot_id}")
                return ApplyOutcome(
                    result=ApplyResult.success,
                    screenshot_path=confirm,
                )
            elif review_btn:
                await review_btn.click()
                await asyncio.sleep(1)
            elif next_btn:
                await next_btn.click()
                await asyncio.sleep(1)
            else:
                # Try any visible Next-like button
                buttons = await page.query_selector_all(".jobs-easy-apply-modal button")
                clicked = False
                for btn in buttons:
                    text = (await btn.inner_text()).lower().strip()
                    if text in ("next", "continue", "review", "submit"):
                        await btn.click()
                        clicked = True
                        await asyncio.sleep(1)
                        break
                if not clicked:
                    break

        screenshot = await self._take_screenshot(page, "screenshots", f"li_incomplete_{shot_id}")
        return ApplyOutcome(
            result=ApplyResult.failed,
            screenshot_path=screenshot,
            error="Could not complete Easy Apply flow",
        )
