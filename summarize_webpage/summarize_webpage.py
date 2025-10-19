#! /usr/bin/env python3

from providers.ollama import OllamaProvider
from providers.openai import OpenAIProvider
from providers.gemini import GeminiProvider
from providers.strategies.openai_api_strategy import OpenAIAPIStrategy
from providers.strategies.gemini_native_strategy import GeminiNativeStrategy
from core.summarizer import summarize_and_display

# --- Discover and Load Providers with Strategies ---

PROVIDERS = [
    OllamaProvider(model_name="llama3.2:latest"),
    OpenAIProvider(model_name="gpt-5-nano"),
    GeminiProvider(strategy=OpenAIAPIStrategy(), model_name="gemini-2.5-flash"),
    GeminiProvider(strategy=GeminiNativeStrategy(), model_name="gemini-2.5-flash"),
]

# --- Main Execution ---

if __name__ == "__main__":
    target_url = "https://www.anthropic.com"
    for provider in PROVIDERS:
        summarize_and_display(provider, target_url)
