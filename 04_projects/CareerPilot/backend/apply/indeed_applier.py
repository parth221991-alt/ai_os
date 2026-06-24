import asyncio
from uuid import uuid4

from playwright.async_api import Page, async_playwright

from apply.base_applier import ApplyOutcome, ApplyResult, BaseApplier
from core.config import get_settings, get_yaml_config


class IndeedApplier(BaseApplier):
    platform = "indeed"

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
                await self._login(page, settings.indeed_email, settings.indeed_password)
                outcome = await self._apply_job(
                    page, job_url, resume_pdf_path, cover_letter, applicant_data, shot_id
                )
            except Exception as e:
                screenshot = await self._take_screenshot(page, "screenshots", f"in_error_{shot_id}")
                outcome = ApplyOutcome(
                    result=ApplyResult.failed,
                    screenshot_path=screenshot,
                    error=str(e),
                )
            finally:
                await browser.close()

        return outcome

    async def _login(self, page: Page, email: str, password: str) -> None:
        await page.goto("https://in.indeed.com/account/login", wait_until="networkidle")
        await asyncio.sleep(2)
        try:
            email_input = await page.query_selector("input[name='__email']")
            if email_input:
                await email_input.fill(email)
                await page.click("[type='submit']")
                await asyncio.sleep(1.5)
            pw_input = await page.query_selector("input[name='__password']")
            if pw_input:
                await pw_input.fill(password)
                await page.click("[type='submit']")
                await page.wait_for_load_state("networkidle")
        except Exception:
            pass
        await asyncio.sleep(2)

    async def _apply_job(
        self,
        page: Page,
        job_url: str,
        resume_path: str,
        cover_letter: str,
        applicant_data: dict,
        shot_id: str,
    ) -> ApplyOutcome:
        await page.goto(job_url, wait_until="networkidle")
        await asyncio.sleep(2)

        apply_btn = await page.query_selector("[id='indeedApplyButton']")
        if not apply_btn:
            return ApplyOutcome(result=ApplyResult.manual_required, notes="Not an Easy Apply job")

        await apply_btn.click()
        await asyncio.sleep(2)

        # Indeed opens application in modal or new page
        max_steps = 8
        for _ in range(max_steps):
            # Upload resume
            resume_input = await page.query_selector("input[type='file']")
            if resume_input:
                await resume_input.set_input_files(resume_path)
                await asyncio.sleep(1)

            # Cover letter
            cover_el = await page.query_selector("textarea[name='coverletter']")
            if cover_el:
                await cover_el.fill(cover_letter[:3000])

            # Common yes/no questions
            for q_id in ["authorizedToWork", "legallyAuthorized", "sponsorship"]:
                yes_radio = await page.query_selector(f"input[id*='{q_id}'][value='yes']")
                if yes_radio:
                    await yes_radio.click()

            continue_btn = await page.query_selector("button[aria-label='Continue']")
            submit_btn = await page.query_selector("button[aria-label='Submit your application']")

            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(2)
                screenshot = await self._take_screenshot(page, "screenshots", f"in_confirm_{shot_id}")
                return ApplyOutcome(result=ApplyResult.success, screenshot_path=screenshot)

            if continue_btn:
                await continue_btn.click()
                await asyncio.sleep(1.5)
            else:
                break

        screenshot = await self._take_screenshot(page, "screenshots", f"in_incomplete_{shot_id}")
        return ApplyOutcome(result=ApplyResult.failed, screenshot_path=screenshot, error="Flow incomplete")
