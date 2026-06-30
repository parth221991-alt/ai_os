"""Standalone worker for on-demand job description fetching.

Run as: python fetch_description_worker.py <url>
Prints the description to stdout (JSON string). Exit code 0 = success, 1 = failure.
Called by the /jobs/{id}/fetch-description API endpoint via subprocess.
"""
import asyncio
import html
import json
import re
import sys


async def fetch(url: str) -> str:
    from playwright.async_api import async_playwright

    description = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        jd_text = await page.evaluate("""() => {
            const scripts = document.querySelectorAll('script[type="application/ld+json"]');
            for (const s of scripts) {
                try {
                    const d = JSON.parse(s.textContent);
                    const data = Array.isArray(d) ? d[0] : d;
                    if (data['@type'] === 'JobPosting' && data.description) {
                        return data.description;
                    }
                } catch(e) {}
            }
            return null;
        }""")

        if jd_text:
            raw = html.unescape(jd_text)
            description = re.sub(r"<[^>]+>", " ", raw).strip()
            description = re.sub(r"\s{2,}", " ", description)[:4000]

        if not description:
            el = await page.query_selector(
                ".show-more-less-html__markup, #job-details, .description__text"
            )
            if el:
                description = (await el.inner_text()).strip()[:4000]

        await browser.close()
    return description


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    url = sys.argv[1]
    try:
        result = asyncio.run(fetch(url))
        print(json.dumps(result))
        sys.exit(0)
    except Exception as e:
        print(json.dumps(""), file=sys.stdout)
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
