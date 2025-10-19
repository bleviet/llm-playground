"""
Integration tests with real LLM APIs.

⚠️  WARNING: These tests make REAL API calls and may incur costs!

Run only when you have:
- Valid API keys in .env
- Budget for API calls
- Need to verify real API integration

Run with: pytest -m integration
Skip with: pytest -m "not integration"
"""

import pytest
import os
from llm_core.providers.ollama import OllamaProvider
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.gemini import GeminiProvider
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy
from llm_core.providers.strategies.gemini_native_strategy import GeminiNativeStrategy


# ============================================================================
# Integration Test Fixtures
# ============================================================================

@pytest.fixture
def skip_if_no_api_keys():
    """Skip test if API keys are not configured."""
    def _check(provider_name):
        key_mapping = {
            "openai": "OPENAI_API_KEY",
            "gemini": "GEMINI_API_KEY",
        }
        key_name = key_mapping.get(provider_name.lower())
        if not key_name or not os.getenv(key_name):
            pytest.skip(f"{key_name} not found - skipping integration test")
    return _check


@pytest.fixture
def integration_test_content():
    """Simple content for integration testing (to minimize API costs)."""
    return "Python is a programming language. It is widely used for web development."


# ============================================================================
# OpenAI Integration Tests
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestOpenAIIntegration:
    """Integration tests for OpenAI provider with real API."""

    def test_openai_summarization_works(
        self,
        skip_if_no_api_keys,
        integration_test_content,
        sample_prompts,
        assert_valid_summary
    ):
        """Test that OpenAI provider can generate real summaries."""
        skip_if_no_api_keys("openai")

        provider = OpenAIProvider(model_name="gpt-4o-mini")  # Use cheaper model
        client = provider.get_client()

        summary = provider.summarize(
            client=client,
            website_content=integration_test_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        # Validate the summary
        assert_valid_summary(summary)
        print(f"\n✅ OpenAI summary: {summary[:100]}...")


# ============================================================================
# Gemini Integration Tests
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestGeminiIntegration:
    """Integration tests for Gemini provider with real API."""

    def test_gemini_with_openai_strategy(
        self,
        skip_if_no_api_keys,
        integration_test_content,
        sample_prompts,
        assert_valid_summary
    ):
        """Test Gemini using OpenAI-compatible API."""
        skip_if_no_api_keys("gemini")

        provider = GeminiProvider(
            strategy=OpenAIAPIStrategy(),
            model_name="gemini-2.0-flash-exp"
        )
        client = provider.get_client()

        summary = provider.summarize(
            client=client,
            website_content=integration_test_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        assert_valid_summary(summary)
        print(f"\n✅ Gemini (OpenAI API) summary: {summary[:100]}...")

    def test_gemini_with_native_strategy(
        self,
        skip_if_no_api_keys,
        integration_test_content,
        sample_prompts,
        assert_valid_summary
    ):
        """Test Gemini using native Google SDK."""
        skip_if_no_api_keys("gemini")

        provider = GeminiProvider(
            strategy=GeminiNativeStrategy(),
            model_name="gemini-2.0-flash-exp"
        )
        client = provider.get_client()

        summary = provider.summarize(
            client=client,
            website_content=integration_test_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        assert_valid_summary(summary)
        print(f"\n✅ Gemini (Native SDK) summary: {summary[:100]}...")


# ============================================================================
# Ollama Integration Tests (Local)
# ============================================================================

@pytest.mark.integration
class TestOllamaIntegration:
    """
    Integration tests for Ollama (local LLM).

    Note: These require Ollama to be running locally.
    """

    @pytest.fixture
    def skip_if_ollama_not_running(self):
        """Skip test if Ollama is not running."""
        import socket

        def is_port_open(host, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0

        if not is_port_open("localhost", 11434):
            pytest.skip("Ollama is not running on localhost:11434")

    def test_ollama_summarization(
        self,
        skip_if_ollama_not_running,
        integration_test_content,
        sample_prompts,
        assert_valid_summary
    ):
        """Test Ollama can generate summaries (if running)."""
        provider = OllamaProvider(model_name="llama3.2:latest")
        client = provider.get_client()

        summary = provider.summarize(
            client=client,
            website_content=integration_test_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        assert_valid_summary(summary)
        print(f"\n✅ Ollama summary: {summary[:100]}...")


# ============================================================================
# Cross-Provider Comparison Tests
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestCrossProviderComparison:
    """
    Compare outputs across multiple providers.

    This is useful for:
    - Verifying all providers work
    - Comparing quality
    - Testing consistency
    """

    @pytest.mark.parametrize("provider_factory", [
        lambda: OpenAIProvider(model_name="gpt-4o-mini"),
        lambda: GeminiProvider(
            strategy=OpenAIAPIStrategy(),
            model_name="gemini-2.0-flash-exp"
        ),
    ])
    def test_all_providers_generate_valid_summaries(
        self,
        provider_factory,
        integration_test_content,
        sample_prompts,
        assert_valid_summary
    ):
        """All providers should generate valid summaries."""
        provider = provider_factory()

        # Skip if API key not available
        if not provider.api_key:
            pytest.skip(f"API key not found for {provider.name}")

        client = provider.get_client()
        summary = provider.summarize(
            client=client,
            website_content=integration_test_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        assert_valid_summary(summary)
        print(f"\n✅ {provider.name} summary: {summary[:100]}...")
