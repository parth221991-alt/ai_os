import asyncio
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import quote_plus

from playwright.async_api import Page, async_playwright

from core.config import get_yaml_config
from scrapers.base import BaseScraper, ScrapedJob

STEALTH_SCRIPT = (
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});"
    "Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});"
)


class LinkedInScraper(BaseScraper):
    platform = "linkedin"

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
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                ],
            )
            context = await browser.new_context(
                user_agent=cfg["scraper"]["user_agent"],
                viewport={"width": 1366, "height": 768},
            )
            context.set_default_timeout(60000)
            await context.add_init_script(STEALTH_SCRIPT)
            page = await context.new_page()

            for query in search_queries:
                if len(jobs) >= max_jobs:
                    break
                results = await self._scrape_query(
                    page, query, location, max_jobs - len(jobs), lookback_days, cfg
                )
                jobs.extend(results)
                await asyncio.sleep(3)

            await browser.close()

        return self.deduplicate(jobs)

    async def _scrape_query(
        self,
        page: Page,
        query: str,
        location: str,
        max_jobs: int,
        lookback_days: int,
        cfg: dict,
    ) -> list[ScrapedJob]:
        # f_TPR values: r86400=24h, r172800=2d, r259200=3d, r604800=7d
        tpr_map = {1: "r86400", 2: "r172800", 3: "r259200", 7: "r604800"}
        tpr = tpr_map.get(lookback_days, "r259200")

        # Public guest search — no login required
        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={quote_plus(query)}"
            f"&location={quote_plus(location)}"
            f"&f_TPR={tpr}"
            f"&position=1&pageNum=0"
        )
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Dismiss sign-in modal if it appears
        try:
            dismiss = await page.query_selector("[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']")
            if dismiss:
                await dismiss.click()
                await asyncio.sleep(1)
        except Exception:
            pass

        # Try scrolling to load more results
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 600)")
            await asyncio.sleep(1)

        jobs: list[ScrapedJob] = []

        # Guest page uses different card selectors than authenticated
        card_selectors = [
            ".job-search-card",
            ".base-card",
            ".jobs-search__results-list li",
            "[data-entity-urn]",
        ]
        cards = []
        for sel in card_selectors:
            cards = await page.query_selector_all(sel)
            if cards:
                break

        for card in cards[:max_jobs]:
            try:
                job = await self._parse_guest_card(card)
                if job:
                    jobs.append(job)
            except Exception:
                continue

        return jobs

    async def _parse_guest_card(self, card) -> Optional[ScrapedJob]:
        title_el = await card.query_selector(
            ".base-search-card__title, h3.base-card__full-link, h3"
        )
        company_el = await card.query_selector(
            ".base-search-card__subtitle, h4, .job-search-card__company-name"
        )
        location_el = await card.query_selector(
            ".job-search-card__location, .base-search-card__metadata span"
        )
        link_el = await card.query_selector("a.base-card__full-link, a[href*='/jobs/view/']")

        if not (title_el and company_el):
            return None

        title = (await title_el.inner_text()).strip()
        company = (await company_el.inner_text()).strip()
        location = (await location_el.inner_text()).strip() if location_el else ""
        href = (await link_el.get_attribute("href") or "") if link_el else ""

        match = re.search(r'/jobs/view/(\d+)', href)
        job_id = match.group(1) if match else hashlib.md5((title + company).encode()).hexdigest()[:12]
        url = f"https://www.linkedin.com/jobs/view/{job_id}/" if match else href

        return ScrapedJob(
            platform=self.platform,
            platform_job_id=job_id,
            url=url,
            title=title,
            company=company,
            location=location,
            description="",  # Description requires job detail page fetch
            is_easy_apply=False,  # Only detectable when logged in
            posted_at=datetime.now(timezone.utc),
        )
