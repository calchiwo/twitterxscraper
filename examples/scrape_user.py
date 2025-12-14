import sys
from twitter_scraper.scraper import TwitterScraper
from twitter_scraper.utils import save_to_csv

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_user.py <username> [limit]")
        sys.exit(1)

    username = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    scraper = TwitterScraper(headless=True)
    tweets = scraper.scrape_user(username, limit=limit)

    save_to_csv(tweets, f"{username}.csv")
    print(f"Scraped {len(tweets)} tweets from @{username}")

if __name__ == "__main__":
    main()
