#! /usr/bin/env python3
"""
Web Summarization Application

This application uses the llm_core providers to summarize web pages.
It demonstrates how to use the shared provider infrastructure.
"""

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

# --- Main Execution ---

if __name__ == "__main__":
    target_url = "https://www.anthropic.com"

    print(f"Summarizing: {target_url}\n")

    for provider in PROVIDERS:
        summarize_and_display(provider, target_url)
