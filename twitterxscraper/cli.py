import argparse
import sys
from twitterxscraper.scraper import TwitterScraper
from twitterxscraper.utils import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Scrape public tweets from X (Twitter)")
    parser.add_argument("username", help="Username to scrape")
    parser.add_argument("--limit", type=int, default=10, help="Number of tweets to grab")
    
    args = parser.parse_args()

    scraper = TwitterScraper(headless=True)
    tweets = scraper.scrape_user(args.username, limit=args.limit)
    if not tweets:
        print(f"No tweets found for @{args.username}")
        return
    
    filename = f"{args.username}.csv"
    save_to_csv(tweets, filename)

    print(f"Starting scraper for: {args.username} (Limit: {args.limit})")
    print(f"Scraped {len(tweets)} tweets from @{args.username} and saved to {filename}")

if __name__ == "__main__":
    main()