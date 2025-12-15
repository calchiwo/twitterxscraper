# twitter-scraper

An open source Python tool for scraping public X (Twitter) tweets using Playwright.

## Why I Built

I built this because I wanted to understand how scraping actually works.

I wanted to deal with a real modern site like X, where the page never fully settles, things keep loading in the background, and you can’t just wait for a simple page load event and hope for the best.

I also wanted to stop hardcoding values everywhere and start writing code that can be reused without opening files and changing strings every time. Passing inputs at runtime, handling limits properly, and structuring things like a real tool mattered to me.

More than anything, I wanted to build something small, real, and finished, not just another experiment that works once and gets abandoned.

## What it can do

At a basic level, this scraper pulls public tweets from any username you give it. It loads the page properly, scrolls to fetch more tweets, and then extracts only the actual tweet text instead of all the surrounding UI noise.

It also grabs timestamps so the data is not just text without context. Once the scrape is done, everything is saved to a CSV file so you can inspect it, analyze it, or use it elsewhere.

Everything runs from the terminal. You pass the username, optionally pass a limit, and the scraper does the rest.

## What it does not do

This scraper does not log into any accounts and it does not touch private profiles. It only works with what is already publicly visible on X.

There are no API keys involved and no attempt to pretend this is more stable than it really is. If X changes their layout in the future, some parts of this will need to be updated. That is just how scraping works.

This is scraping. Stuff breaks sometimes. That’s part of it.

## Tech used

- Python  
- Playwright  
- Pandas  

I just used tools that get the job done.

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
If you use it for purposes like commercial uses you must inform.
## Final thoughts

If you are learning scraping, packaging, or just want to understand how things work under the hood, feel free to explore the code.

If it helps you, cool.

If it breaks, fix it!. That’s the fun part tbh.

Byeeee.
