"""Live Unstop internship importer that preserves each listing's direct URL."""

import asyncio
import hashlib
import logging
from datetime import date, timedelta

from app.ingestion.base import RawOpportunity

logger = logging.getLogger(__name__)

_URL = "https://unstop.com/internships"
_MAX_LISTINGS = 25


class UnstopLiveInternshipConnector:
    """Fetch current Unstop internship cards instead of publishing demo links."""

    source_id = "unstop_live"

    def fetch(self) -> list[RawOpportunity]:
        try:
            records = asyncio.run(self._fetch_records())
        except Exception as exc:
            logger.warning("Unstop live internship import failed: %s", exc)
            return []

        return [
            RawOpportunity(
                external_id=f"unstop-live-{hashlib.sha256(item['url'].encode()).hexdigest()[:24]}",
                source="unstop",
                title=item["title"],
                description=item["description"],
                amount_min=None,
                amount_max=None,
                deadline=date.today() + timedelta(days=30),
                eligibility_rules={"states": ["ALL"]},
                documents_required=["resume"],
                application_url=item["url"],
                state_filter=["ALL"],
                tags=["unstop", "live"],
                raw_data={"company": item.get("company"), "location": item.get("location")},
            )
            for item in records
        ]

    async def _fetch_records(self) -> list[dict]:
        from playwright.async_api import async_playwright

        async with async_playwright() as browser_api:
            browser = await browser_api.chromium.launch(headless=True)
            context = None
            try:
                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    )
                )
                page = await context.new_page()
                await page.goto(_URL, wait_until="domcontentloaded", timeout=30_000)
                try:
                    await page.wait_for_load_state("networkidle", timeout=12_000)
                except Exception:
                    pass
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
                records = await page.evaluate(f"""
                    () => Array.from(document.querySelectorAll('a[href*="/internships/"]'))
                      .map((link) => {{
                        const href = link.getAttribute('href') || '';
                        const card = link.closest('app-competition-listing, article, li') || link.parentElement;
                        const text = (card?.innerText || link.innerText || '').trim();
                        const lines = text.split('\\n').map(x => x.trim()).filter(Boolean);
                        return {{ href, title: (link.innerText || lines[0] || '').trim(), text, lines }};
                      }})
                      .filter(item => item.href !== '/internships' && item.title)
                      .slice(0, {_MAX_LISTINGS})
                """)
            finally:
                if context is not None:
                    await context.close()
                await browser.close()

        seen: set[str] = set()
        result = []
        for item in records:
            url = item["href"]
            url = f"https://unstop.com{url}" if url.startswith("/") else url
            if url in seen:
                continue
            seen.add(url)
            lines = item.get("lines") or []
            result.append({
                "url": url,
                "title": item["title"][:512],
                "description": item.get("text", "")[:2_000],
                "company": lines[1] if len(lines) > 1 else None,
                "location": None,
            })
        return result
