"""
LLM Core - Reusable LLM Provider Infrastructure

This package provides a unified interface for working with multiple LLM providers
using the Strategy and Provider design patterns.
"""

__version__ = "0.1.0"

from llm_core.providers.base_provider import BaseProvider
from llm_core.providers.ollama import OllamaProvider
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.gemini import GeminiProvider

__all__ = [
    "BaseProvider",
    "OllamaProvider",
    "OpenAIProvider",
    "GeminiProvider",
]
