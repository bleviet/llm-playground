#! /usr/bin/env python3
"""
Web Summarization Application

This application uses the llm_core providers to summarize web pages.
It demonstrates how to use the shared provider infrastructure.

Usage:
    python summarize_webpage.py [URL]
    python summarize_webpage.py https://www.example.com
    
If no URL is provided, defaults to https://www.anthropic.com
"""

import click

# Import from llm_core (shared infrastructure)
from llm_core.providers.ollama import OllamaProvider
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.gemini import GeminiProvider
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy
from llm_core.providers.strategies.gemini_native_strategy import GeminiNativeStrategy

# Import application-specific code
from core.summarizer import summarize_and_display

# --- Discover and Load Providers with Strategies ---

# --- Configure Providers ---

PROVIDERS = [
    OllamaProvider(model_name="llama3.2:latest"),
    OpenAIProvider(model_name="gpt-5-nano"),
    GeminiProvider(strategy=OpenAIAPIStrategy(), model_name="gemini-2.5-flash"),
    GeminiProvider(strategy=GeminiNativeStrategy(), model_name="gemini-2.5-flash"),
]


@click.command()
@click.argument(
    'url',
    default='https://www.anthropic.com',
    type=str
)
@click.option(
    '--provider',
    '-p',
    type=click.Choice(['ollama', 'openai', 'gemini-openai', 'gemini-native', 'all'], case_sensitive=False),
    default='all',
    help='Choose which LLM provider to use for summarization'
)
def main(url: str, provider: str):
    """
    Summarize a webpage using LLM providers.
    
    URL: The webpage URL to summarize (defaults to https://www.anthropic.com)
    
    Examples:
        \b
        # Summarize default URL with all providers
        python summarize_webpage.py
        
        \b
        # Summarize specific URL
        python summarize_webpage.py https://www.python.org
        
        \b
        # Use only OpenAI provider
        python summarize_webpage.py https://example.com --provider openai
    """
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        click.echo(click.style(f"⚠️  Invalid URL: {url}", fg='red', bold=True))
        click.echo("URL must start with http:// or https://")
        raise click.Abort()
    
    # Filter providers based on user choice
    provider_map = {
        'ollama': [PROVIDERS[0]],
        'openai': [PROVIDERS[1]],
        'gemini-openai': [PROVIDERS[2]],
        'gemini-native': [PROVIDERS[3]],
        'all': PROVIDERS
    }
    
    selected_providers = provider_map[provider.lower()]
    
    click.echo(click.style(f"\n🌐 Summarizing: {url}", fg='cyan', bold=True))
    click.echo(click.style(f"📊 Using {len(selected_providers)} provider(s)\n", fg='cyan'))
    
    for llm_provider in selected_providers:
        summarize_and_display(llm_provider, url)


# --- Main Execution ---

if __name__ == "__main__":
    main()
