import asyncio
import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import quote_plus

from playwright.async_api import Page, async_playwright

from core.config import get_yaml_config
from scrapers.base import BaseScraper, ScrapedJob


class IndeedScraper(BaseScraper):
    platform = "indeed"

    async def scrape(
        self,
        search_queries: list[str],
        location: str = "India",
        max_jobs: int = 100,
        lookback_days: int = 3,
    ) -> list[ScrapedJob]:
        jobs: list[ScrapedJob] = []
        cfg = get_yaml_config()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=cfg["scraper"]["headless"],
                args=["--no-sandbox"],
            )
            context = await browser.new_context(
                user_agent=cfg["scraper"]["user_agent"],
            )
            page = await context.new_page()

            for query in search_queries:
                if len(jobs) >= max_jobs:
                    break
                results = await self._scrape_query(
                    page, query, location, max_jobs - len(jobs), lookback_days
                )
                jobs.extend(results)
                await asyncio.sleep(4)

            await browser.close()

        return self.deduplicate(jobs)

    async def _scrape_query(
        self,
        page: Page,
        query: str,
        location: str,
        max_jobs: int,
        lookback_days: int,
    ) -> list[ScrapedJob]:
        jobs = []
        # fromage: days since posting
        fromage = min(lookback_days, 14)
        url = (
            f"https://in.indeed.com/jobs"
            f"?q={quote_plus(query)}"
            f"&l={quote_plus(location)}"
            f"&fromage={fromage}"
        )
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)

        cards = await page.query_selector_all("[data-jk]")
        for card in cards[:max_jobs]:
            try:
                job = await self._parse_card(card)
                if job:
                    jobs.append(job)
                    await asyncio.sleep(0.5)
            except Exception:
                continue

        return jobs

    async def _parse_card(self, card) -> ScrapedJob | None:
        title_el = await card.query_selector("[class*='jobTitle'] a")
        company_el = await card.query_selector("[data-testid='company-name']")
        location_el = await card.query_selector("[data-testid='text-location']")
        snippet_el = await card.query_selector("[class*='underShelfFooter']")

        if not title_el:
            return None

        title = (await title_el.inner_text()).strip()
        company = (await company_el.inner_text()).strip() if company_el else ""
        location = (await location_el.inner_text()).strip() if location_el else ""
        snippet = (await snippet_el.inner_text()).strip() if snippet_el else ""

        job_id = await card.get_attribute("data-jk") or ""
        url = f"https://in.indeed.com/viewjob?jk={job_id}"

        is_easy = False
        try:
            easy_el = await card.query_selector("[aria-label='Easily apply']")
            is_easy = easy_el is not None
        except Exception:
            pass

        return ScrapedJob(
            platform=self.platform,
            platform_job_id=job_id,
            url=url,
            title=title,
            company=company,
            location=location,
            description=snippet,
            is_easy_apply=is_easy,
            posted_at=datetime.now(timezone.utc),
        )
