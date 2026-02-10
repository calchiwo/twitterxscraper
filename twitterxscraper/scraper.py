from __future__ import annotations

import logging
from typing import Optional
from contextlib import contextmanager

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Page
)

logger = logging.getLogger(__name__)


class ScraperConfig:
    def __init__(
        self,
        headless: bool = True,
        timeout: int = 90000,
        user_agent: Optional[str] = None,
    ):
        self.headless = headless
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        )


class TwitterScraper:
    def __init__(self, config: Optional[ScraperConfig] = None):
        self.config = config or ScraperConfig()

    @contextmanager
    def _browser_context(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=self.config.headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent=self.config.user_agent,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )

        page = context.new_page()

        try:
            yield page
        finally:
            context.close()
            browser.close()
            playwright.stop()

    def _navigate_safely(self, page: Page, url: str) -> bool:
        strategies = [
            "load",
            "domcontentloaded",
            "networkidle",
            "commit",
        ]

        for strategy in strategies:
            try:
                page.goto(url, wait_until=strategy, timeout=self.config.timeout)
                return True
            except PlaywrightTimeoutError:
                continue
            except Exception:
                continue

        return False

    def _extract_tweets(self, page: Page, username: str, limit: int) -> list[dict]:
        tweets = []

        try:
            page.wait_for_selector("article", timeout=15000)
        except PlaywrightTimeoutError:
            return tweets

        # Scroll
        for _ in range(5):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(1500)

        locator = page.locator("article")
        count = locator.count()

        for i in range(count):
            if len(tweets) >= limit:
                break

            article = locator.nth(i)

            try:
                text_locator = article.locator('[data-testid="tweetText"]')
                if text_locator.count() == 0:
                    continue

                text = text_locator.first.inner_text(timeout=5000)

                time_locator = article.locator("time")
                timestamp = None
                if time_locator.count() > 0:
                    timestamp = time_locator.first.get_attribute("datetime")

                tweets.append({
                    "username": username,
                    "text": text.strip(),
                    "timestamp": timestamp,
                })

            except Exception:
                continue

        return tweets

    def scrape_user(self, username: str, limit: int = 10) -> list[dict]:
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")

        if limit <= 0:
            raise ValueError("Limit must be greater than 0")

        username = username.strip().lstrip("@")
        url = f"https://x.com/{username}"

        with self._browser_context() as page:
            if not self._navigate_safely(page, url):
                return []

            page.wait_for_timeout(3000)
            return self._extract_tweets(page, username, limit)