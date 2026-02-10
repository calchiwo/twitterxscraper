# TwitterXScraper

A Python CLI tool for scraping public X (Twitter) profile tweets using Playwright and exporting structured results to a CSV file without requiring API keys.

[![PyPI Version](https://img.shields.io/pypi/v/twitterxscraper?color=blue)](https://pypi.org/project/twitterxscraper/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/twitterxscraper?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/twitterxscraper)
[![Python](https://img.shields.io/pypi/pyversions/twitterxscraper?logo=python&logoColor=white)](https://pypi.org/project/twitterxscraper/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why this exists

I needed a simple way to pull public tweets from X without using the official API, managing authentication tokens, or dealing with rate limits.

So I wrote this CLI tool that accepts a username, opens a Chromium browser using Playwright, scrolls a profile dynamically, extracts tweet text and timestamps, and exports everything into a CSV file.


## Features

- Scrape public tweets from any username
- Automatically scroll to load more tweets
- Extract clean tweet text
- Extract timestamps
- Save results to CSV
- Headless and headful modes
- Configurable tweet limit
- No API keys required
- No authentication

## How It Works

The scraper launches a Chromium browser using Playwright, navigates to a public X profile, waits for dynamic content to stabilize, scrolls to trigger additional tweet loading, and extracts structured data from the DOM.

## Installation

```bash
pip install twitterxscraper
python -m playwright install chromium
```

## Clone this repository

```bash
git clone https://github.com/calchiwo/twitterxscraper.git
cd twitterxscraper
```

Install dependencies.

```bash
python -m pip install -e .
python -m playwright install chromium
```

## Usage

### Run the CLI and pass a username:

```bash
twitterxscraper <username>
```

Example:

```bash
twitterxscraper elonmusk
```

This creates a CSV file named after the username: `<username>.csv`.

### Set tweet limit:

```bash
twitterxscraper <username> --limit 15
```

Example:

```bash
twitterxscraper elonmusk --limit 15
```

### Run in a visible browser mode (debugging)

```bash
twitterxscraper <username> --headful
```

### Run as a module
You can also run it using:
```bash
python -m twitterxscraper <username>
```

## Output
The scraper exports a CSV file with the following columns:

- username
- text
- timestamp

## Exit Codes

- 0 → Successful scrape
- 1 → No tweets found or validation error

## Using it in your own code

You can also run directly as a Python class.

```python
from twitterxscraper import TwitterScraper

scraper = TwitterScraper()
tweets = scraper.scrape_user("<username>", limit=10)

print(tweets)
```

## Requirements
- Python 3.8+
- Chromium browser installed via `python -m playwright install chromium`


## Limitations

- Only works on public profiles
- No login support
- No private accounts
- May break if X changes layout
- Uses a Chromium browser with Playwright
- X is a dynamic platform so layout changes may require selector updates
- Scraping behavior may vary depending on network conditions and X's anti-bot mechanisms

## Tech stack used

- Python
- Playwright
- Pandas
- Rich (CLI formatting)

## Disclaimer
This project is intended for educational and research purposes only.

Respect platform terms of service and applicable laws. Use responsibly.

## License
MIT

## Author

[Caleb Wodi](https://github.com/calchiwo)