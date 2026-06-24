import asyncio
from uuid import uuid4

from playwright.async_api import Page, async_playwright

from apply.base_applier import ApplyOutcome, ApplyResult, BaseApplier
from core.config import get_settings, get_yaml_config


class NaukriApplier(BaseApplier):
    platform = "naukri"

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
                await self._login(page, settings.naukri_email, settings.naukri_password)
                outcome = await self._apply_job(
                    page, job_url, resume_pdf_path, cover_letter, applicant_data, shot_id
                )
            except Exception as e:
                screenshot = await self._take_screenshot(page, "screenshots", f"nk_error_{shot_id}")
                outcome = ApplyOutcome(
                    result=ApplyResult.failed,
                    screenshot_path=screenshot,
                    error=str(e),
                )
            finally:
                await browser.close()

        return outcome

    async def _login(self, page: Page, email: str, password: str) -> None:
        await page.goto("https://www.naukri.com/", wait_until="networkidle")
        await asyncio.sleep(2)
        try:
            login_btn = await page.query_selector("[title='Jobseeker Login']")
            if login_btn:
                await login_btn.click()
                await asyncio.sleep(1)
            await page.fill("input[placeholder='Enter your active Email ID / Username']", email)
            await page.fill("input[placeholder='Enter your password']", password)
            await page.click("button[type='submit']")
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

        apply_btn = await page.query_selector("[class*='apply-button']")
        if not apply_btn:
            apply_btn = await page.query_selector("button[contains(text(), 'Apply')]")
        if not apply_btn:
            return ApplyOutcome(result=ApplyResult.manual_required, notes="No apply button found")

        await apply_btn.click()
        await asyncio.sleep(2)

        # Naukri may open a new tab for the application
        pages = page.context.pages
        if len(pages) > 1:
            page = pages[-1]
            await page.wait_for_load_state("networkidle")

        # Cover letter / message
        msg_el = await page.query_selector("textarea[placeholder*='message']")
        if msg_el:
            await msg_el.fill(cover_letter[:1000])

        # Confirm apply
        confirm_btn = await page.query_selector("[class*='apply-now']")
        if confirm_btn:
            await confirm_btn.click()
            await asyncio.sleep(2)

        screenshot = await self._take_screenshot(page, "screenshots", f"nk_applied_{shot_id}")
        return ApplyOutcome(result=ApplyResult.success, screenshot_path=screenshot)
