import argparse
import sys
from rich.console import Console
from rich.status import Status
from rich.table import Table
from rich.panel import Panel

from twitterxscraper.scraper import TwitterScraper
from twitterxscraper.utils import save_to_csv

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Scrape public tweets from X (Twitter)")
    parser.add_argument("username", help="Username to scrape")
    parser.add_argument("--limit", type=int, default=10, help="Number of tweets to grab")
    args = parser.parse_args()

    # Welcome Header
    console.print(Panel.fit(
        f"[bold blue]TwitterXScraper[/bold blue]\n[dim]Target: @{args.username} | Limit: {args.limit}[/dim]",
        border_style="blue"
    ))

    # Interactive Status Spinner
    with console.status(f"[bold green]Initializing Playwright and reaching X...", spinner="dots") as status:
        try:
            scraper = TwitterScraper(headless=True)
            
            status.update(status=f"[bold cyan]Scraping tweets from @{args.username}...")
            tweets = scraper.scrape_user(args.username, limit=args.limit)
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            return

    # Handling Results
    if not tweets:
        console.print(f"[bold yellow]![/bold yellow] No public tweets found for [bold]@{args.username}[/bold]")
        return
    
    # Save Process
    filename = f"{args.username}.csv"
    with console.status("[bold magenta]Saving data to CSV...", spinner="bouncingBar"):
        save_to_csv(tweets, filename)

    # Visual Summary Table
    console.print("\n[bold green]✓ Scraping Complete![/bold green]")
    
    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Attribute", style="dim")
    summary_table.add_column("Value")
    
    summary_table.add_row("User", f"@{args.username}")
    summary_table.add_row("Tweets Collected", str(len(tweets)))
    summary_table.add_row("Saved To", filename)
    
    console.print(summary_table)

if __name__ == "__main__":
    main()