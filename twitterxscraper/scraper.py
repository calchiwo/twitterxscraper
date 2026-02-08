from playwright.sync_api import sync_playwright


class TwitterScraper:
    def __init__(self, headless=True):
        self.headless = headless

    def scrape_user(self, username, limit=10):
        url = f"https://x.com/{username}"
        tweets = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # Scroll to load more tweets
            for _ in range(3):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(2000)

            page.wait_for_selector("article", timeout=60000)

            articles = page.locator("article")

            for i in range(articles.count()):
                if len(tweets) >= limit:
                    break

                article = articles.nth(i)

                try:
                    text_locator = article.locator('div[data-testid="tweetText"]')
                    if not text_locator.count():
                        continue

                    text = text_locator.inner_text()

                    time_locator = article.locator("time")
                    timestamp = (
                        time_locator.get_attribute("datetime")
                        if time_locator.count()
                        else None
                    )

                    tweets.append({
                        "username": username,
                        "text": text,
                        "timestamp": timestamp,
                    })

                except Exception:
                    continue

            browser.close()

        return tweets

