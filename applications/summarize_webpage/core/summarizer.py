"""
Summarization workflow orchestration.

This module handles the business logic of fetching, summarizing, and displaying
website content using LLM providers from llm_core.
"""

from scraper import fetch_website_contents
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

system_prompt = """
You are a helpful assistant that analyzes website content and provides clear, concise summaries.
Focus on the main content and key information, ignoring navigation elements, headers, and footers.
Provide your response in markdown format without wrapping it in code blocks.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.
"""


def summarize_and_display(provider, url):
    """
    Fetches content, summarizes it, and prints the result in a rich format.

    This function uses the provider infrastructure from llm_core but handles
    the application-specific workflow of web summarization.

    Args:
        provider: An instance of BaseProvider from llm_core
        url: The URL to summarize
    """

    if not provider.api_key:
        console.print(Panel(f"API key for [bold yellow]{provider.name}[/bold yellow] not found. Skipping.", title="[bold red]Error[/bold red]", border_style="red"))
        return

    with console.status(f"[bold green]Querying {provider.name}...[/bold green]"):
        client = provider.get_client()
        website_content = fetch_website_contents(url)

        if website_content.startswith("Error fetching website content"):
            console.print(Panel(website_content, title="[bold red]Scraping Error[/bold red]", border_style="red"))
            return

        summary = provider.summarize(client, website_content, system_prompt, user_prompt_prefix)

    # Display the summary in a panel
    panel_title = f"[bold cyan]{provider.name}[/bold cyan] ([italic]{provider.model}[/italic])"
    console.print(Panel(Markdown(summary), title=panel_title, border_style="green", expand=False))
    console.print()
