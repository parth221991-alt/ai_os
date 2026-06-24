import asyncio
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import quote_plus

from playwright.async_api import Page, async_playwright

from core.config import get_settings, get_yaml_config
from scrapers.base import BaseScraper, ScrapedJob


class NaukriScraper(BaseScraper):
    platform = "naukri"

    async def scrape(
        self,
        search_queries: list[str],
        location: str = "India",
        max_jobs: int = 100,
        lookback_days: int = 3,
    ) -> list[ScrapedJob]:
        jobs: list[ScrapedJob] = []
        cfg = get_yaml_config()
        settings = get_settings()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=cfg["scraper"]["headless"],
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--start-maximized",
                ],
            )
            context = await browser.new_context(
                user_agent=cfg["scraper"]["user_agent"],
                viewport={"width": 1366, "height": 768},
            )
            context.set_default_timeout(60000)
            await context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            page = await context.new_page()

            await self._login(page, settings.naukri_email, settings.naukri_password)

            for query in search_queries:
                if len(jobs) >= max_jobs:
                    break
                results = await self._scrape_query(
                    page, query, location, max_jobs - len(jobs), lookback_days
                )
                jobs.extend(results)
                await asyncio.sleep(3)

            await browser.close()

        return self.deduplicate(jobs)

    async def _login(self, page: Page, email: str, password: str) -> None:
        await page.goto("https://www.naukri.com/nlogin/login", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Wait for any input to appear, then try known selectors
        await asyncio.sleep(3)
        email_selectors = [
            "input[placeholder*='Email']",
            "input[placeholder*='Username']",
            "#usernameField",
            "#loginEmail",
            "input[type='email']",
            "input[name='username']",
            "input[type='text']",
        ]
        filled = False
        for sel in email_selectors:
            try:
                el = await page.wait_for_selector(sel, state="visible", timeout=5000)
                if el:
                    await el.fill(email)
                    filled = True
                    break
            except Exception:
                continue
        if not filled:
            # Debug: dump page HTML snippet
            html = await page.content()
            raise RuntimeError(f"Could not find Naukri email input. Page title: {await page.title()}")

        password_selectors = [
            "input[type='password']",
            "input[placeholder*='password']",
            "#loginPasswd",
            "#currentPassword",
        ]
        for sel in password_selectors:
            el = await page.query_selector(sel)
            if el:
                await el.fill(password)
                break

        await page.click("button[type='submit']")
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(3)

    async def _scrape_query(
        self,
        page: Page,
        query: str,
        location: str,
        max_jobs: int,
        lookback_days: int,
    ) -> list[ScrapedJob]:
        jobs = []
        encoded_query = quote_plus(query)
        encoded_location = quote_plus(location)
        # freshness: 1=24h, 3=3days, 7=7days, 15=15days
        freshness = min(lookback_days, 15)
        url = (
            f"https://www.naukri.com/{encoded_query.replace('+', '-')}-jobs"
            f"?k={encoded_query}&l={encoded_location}&freshness={freshness}"
        )
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Naukri uses different card classes across redesigns
        cards = await page.query_selector_all(".jobTuple, .job-tuple, article.jobTupleHeader, .srp-jobtuple-wrapper")
        for card in cards[:max_jobs]:
            try:
                job = await self._parse_card(card)
                if job:
                    jobs.append(job)
            except Exception:
                continue

        return jobs

    async def _parse_card(self, card) -> Optional[ScrapedJob]:
        title_el = await card.query_selector(".title")
        company_el = await card.query_selector(".companyInfo .subTitle")
        location_el = await card.query_selector(".location")
        desc_el = await card.query_selector(".job-description")
        link_el = await card.query_selector("a.title")

        if not (title_el and company_el and link_el):
            return None

        title = (await title_el.inner_text()).strip()
        company = (await company_el.inner_text()).strip()
        location = (await location_el.inner_text()).strip() if location_el else ""
        description = (await desc_el.inner_text()).strip() if desc_el else ""
        href = await link_el.get_attribute("href") or ""

        job_id = hashlib.md5(href.encode()).hexdigest()[:16]
        match = re.search(r'-(\d+)\.htm', href)
        if match:
            job_id = match.group(1)

        return ScrapedJob(
            platform=self.platform,
            platform_job_id=job_id,
            url=href if href.startswith("http") else f"https://www.naukri.com{href}",
            title=title,
            company=company,
            location=location,
            description=description,
            posted_at=datetime.now(timezone.utc),
        )
