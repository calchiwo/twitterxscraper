import argparse
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pandas as pd

from twitterxscraper.scraper import TwitterScraper, ScraperConfig


console = Console()


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def save_to_csv(tweets: list[dict], filename: str) -> None:
    if not tweets:
        return
    df = pd.DataFrame(tweets)
    df.to_csv(filename, index=False, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape public tweets from X (Twitter)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("username", help="Username to scrape (with or without @)")
    parser.add_argument("--limit", type=int, default=10, help="Number of tweets")
    parser.add_argument("--headful", action="store_true", help="Run browser visibly")
    parser.add_argument("--timeout", type=int, default=90000)
    parser.add_argument("--output", type=str)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    setup_logging(args.verbose)

    headless = not args.headful

    username = args.username.strip().lstrip("@")
    output_file = args.output or f"{username}.csv"

    console.print(Panel.fit(
        f"[bold blue]TwitterXScraper[/bold blue]\n"
        f"[dim]Target: @{username} | Limit: {args.limit} | "
        f"Mode: {'Headless' if headless else 'Headful'}[/dim]",
        border_style="blue"
    ))

    config = ScraperConfig(
        headless=headless,
        timeout=args.timeout,
    )

    try:
        with console.status(
            "[bold green]Launching browser...",
            spinner="dots"
        ) as status:
            scraper = TwitterScraper(config)
            status.update(f"[bold cyan]Scraping @{username}...")
            tweets = scraper.scrape_user(username, limit=args.limit)

    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        return 1
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if args.verbose:
            console.print_exception()
        return 1

    if not tweets:
        console.print(f"[bold yellow]![/bold yellow] No tweets found for @{username}")
        console.print("[dim]Try --headful --verbose for debugging[/dim]")
        return 1

    with console.status("[bold magenta]Saving CSV...", spinner="bouncingBar"):
        save_to_csv(tweets, output_file)

    console.print("\n[bold green]✓ Scraping Complete[/bold green]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attribute", style="dim", no_wrap=True)
    table.add_column("Value")

    table.add_row("User", f"@{username}")
    table.add_row("Tweets", str(len(tweets)))
    table.add_row("Saved To", output_file)
    table.add_row("File Size", f"{Path(output_file).stat().st_size:,} bytes")

    console.print(table)

    return 0


if __name__ == "__main__":
    sys.exit(main())