# twitter-scraper

An open source Python tool for scraping public X (Twitter) tweets using Playwright.

## Why I built this

I wanted to learn a few things properly like,

- How web scraping actually works  
- How to deal with dynamic pages like X  
- How to structure a Python project properly  
- How to avoid hardcoding and build something reusable  

## What it can do

- Scrape public tweets from any username  
- Load tweets by scrolling  
- Extract clean tweet text  
- Extract timestamps  
- Save results to CSV
- Run fully from the terminal  

## What it does not do

- No login  
- No private accounts  
- No API keys  
- No guarantee X won’t change things later

## Tech used

- Python  
- Playwright  
- Pandas  

i just used tools that get the job done.

## Setup

Clone the repo.

```bash
    git clone https://github.com/calchiwo/twitter-scraper.git
    cd twitter-scraper
```

Install dependencies.

```bash
    python -m pip install -r requirements.txt
    python -m playwright install chromium
```

## Usage

Run the example script and pass a username.

```bash
    python examples/scrape_user.py elonmusk
```

With a custom limit.

```bash
    python examples/scrape_user.py elonmusk 15
```

This creates a CSV file named after the username, for example `elonmusk.csv`.  
CSV files are ignored by git and stay local.

## Using it in your own code

You can also use it directly as a Python class.

```python
    from twitter_scraper.scraper import TwitterScraper

    scraper = TwitterScraper()
    tweets = scraper.scrape_user("orcdev", limit=10)

    print(tweets)
```

Nothing runs on import. Also scraping only happens when you call the method.

## Notes

X never becomes network idle, so this uses domcontentloaded.  
Playwright launches a real browser.  
The first run might feel slow. That’s normal.  
If X changes their layout, selectors may need updates.

This is part of the game.

## Disclaimer

This project is for educational and research purposes only.

Be responsible.  
Respect platform rules.  
Do not abuse it.

## Final thoughts

If you are learning scraping, packaging, or just want to understand how things work under the hood, feel free to explore the code.

If it helps you, cool.

If it breaks, fix it!. That’s the fun part tbh.

Byeeee
