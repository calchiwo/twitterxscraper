from playwright.sync_api import sync_playwright


class TwitterScraper:
    """
    Scrapes public tweets from an X (Twitter) profile.
    """

    def __init__(self, headless: bool = True):
        self.headless = headless

    def scrape_user(self, username: str, limit: int = 10):
        """
        Scrape public tweets from a given username.

        :param username: X username without @
        :param limit: Maximum number of tweets to collect
        :return: List of tweet dictionaries
        """
        if not username:
            raise ValueError("Username must not be empty")

        if limit <= 0:
            raise ValueError("Limit must be greater than 0")

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

            try:
                page.wait_for_selector("article", timeout=60000)
            except Exception:
                browser.close()
                return tweets

            articles = page.locator("article")

            for i in range(articles.count()):
                if len(tweets) >= limit:
                    break

                article = articles.nth(i)

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

            browser.close()

        return tweets