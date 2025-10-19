"""
Unit tests for API strategies.

Strategies encapsulate HOW to communicate with different APIs.
Testing them separately from providers ensures:
- Strategy logic is correct
- Providers can safely switch strategies
- Easy to add new strategies

Run with: pytest llm_core/tests/test_strategies.py
"""

import pytest
from unittest.mock import Mock, MagicMock
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy
from llm_core.providers.strategies.gemini_native_strategy import GeminiNativeStrategy


# ============================================================================
# OpenAI API Strategy Tests
# ============================================================================

@pytest.mark.unit
class TestOpenAIAPIStrategy:
    """Test OpenAI-compatible API strategy."""

    def test_strategy_initialization(self):
        """Strategy should initialize without errors."""
        strategy = OpenAIAPIStrategy()
        assert strategy is not None

    def test_get_client_creates_openai_client(self):
        """get_client should create an OpenAI client instance."""
        strategy = OpenAIAPIStrategy()

        # Create a mock provider
        mock_provider = Mock()
        mock_provider.api_key = "test-key"
        mock_provider.base_url = None

        client = strategy.get_client(mock_provider)

        from openai import OpenAI
        assert isinstance(client, OpenAI)

    def test_get_client_with_custom_base_url(self):
        """Test creating OpenAI client with custom base URL (e.g., for Ollama)."""
        strategy = OpenAIAPIStrategy()

        # Mock provider with custom base URL
        mock_provider = Mock()
        mock_provider.api_key = "test-key"
        mock_provider.base_url = "http://localhost:11434/v1"

        client = strategy.get_client(mock_provider)

        # OpenAI client returns URL object, convert to string and strip trailing slash
        assert str(client.base_url).rstrip('/') == "http://localhost:11434/v1"

    def test_summarize_calls_api_correctly(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """summarize should format messages and call API correctly."""
        strategy = OpenAIAPIStrategy()

        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        mock_provider.model = "test-model"

        result = strategy.summarize(
            provider=mock_provider,
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        # Verify API was called
        assert mock_openai_client.chat.completions.create.called

        # Verify result
        assert result == "This is a test summary."

    def test_summarize_message_structure(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """Verify that messages are structured correctly."""
        strategy = OpenAIAPIStrategy()

        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        mock_provider.model = "test-model"

        strategy.summarize(
            provider=mock_provider,
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]

        # Should have system and user messages
        assert len(messages) == 2

        # System message
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == sample_prompts["system_prompt"]

        # User message
        assert messages[1]["role"] == "user"
        expected_content = sample_prompts["user_prompt_prefix"] + sample_website_content
        assert messages[1]["content"] == expected_content

    def test_summarize_error_handling(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """Strategy should handle API errors gracefully."""
        # Configure mock to raise exception
        mock_openai_client.chat.completions.create.side_effect = Exception("Network error")

        strategy = OpenAIAPIStrategy()
        mock_provider = Mock()
        mock_provider.name = "TestProvider"

        result = strategy.summarize(
            provider=mock_provider,
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        # Should return error message with provider name
        assert "error" in result.lower() or "Error" in result
        assert "TestProvider" in result


# ============================================================================
# Gemini Native Strategy Tests
# ============================================================================

@pytest.mark.unit
class TestGeminiNativeStrategy:
    """Test Google's native Gemini SDK strategy."""

    def test_strategy_initialization(self):
        """Strategy should initialize without errors."""
        strategy = GeminiNativeStrategy()
        assert strategy is not None

    def test_get_client_creates_gemini_client(self):
        """get_client should create a Gemini GenerativeModel instance."""
        strategy = GeminiNativeStrategy()

        mock_provider = Mock()
        mock_provider.api_key = "test-gemini-key"
        mock_provider.model = "gemini-pro"

        client = strategy.get_client(mock_provider)

        # Should return a GenerativeModel instance
        import google.generativeai as genai
        assert isinstance(client, genai.GenerativeModel)

    def test_summarize_calls_api_correctly(
        self,
        mock_gemini_client,
        sample_website_content,
        sample_prompts
    ):
        """summarize should format prompt and call API correctly."""
        strategy = GeminiNativeStrategy()

        mock_provider = Mock()
        mock_provider.name = "Gemini"

        result = strategy.summarize(
            provider=mock_provider,
            client=mock_gemini_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        # Verify API was called
        assert mock_gemini_client.generate_content.called

        # Verify result
        assert result == "This is a test Gemini summary."

    def test_summarize_prompt_formatting(
        self,
        mock_gemini_client,
        sample_website_content,
        sample_prompts
    ):
        """Verify that Gemini prompt is formatted correctly."""
        strategy = GeminiNativeStrategy()

        mock_provider = Mock()
        mock_provider.name = "Gemini"

        strategy.summarize(
            provider=mock_provider,
            client=mock_gemini_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )

        call_args = mock_gemini_client.generate_content.call_args
        prompt = call_args[0][0]

        # Gemini combines system and user prompts
        assert sample_prompts["system_prompt"] in prompt
        assert sample_prompts["user_prompt_prefix"] in prompt
        assert sample_website_content in prompt


# ============================================================================
# Strategy Comparison Tests
# ============================================================================

@pytest.mark.unit
class TestStrategyInterface:
    """
    BEST PRACTICE: Test that all strategies implement the same interface.

    This ensures strategies are truly interchangeable.
    """

    @pytest.mark.parametrize("strategy_class", [
        OpenAIAPIStrategy,
        GeminiNativeStrategy,
    ])
    def test_strategy_has_required_methods(self, strategy_class):
        """All strategies should implement get_client and summarize."""
        strategy = strategy_class()

        assert hasattr(strategy, 'get_client')
        assert hasattr(strategy, 'summarize')
        assert callable(strategy.get_client)
        assert callable(strategy.summarize)

    def test_strategies_are_interchangeable(self):
        """
        ARCHITECTURAL TEST: Strategies should be swappable.

        This tests the Strategy Pattern implementation.
        """
        from llm_core.providers.gemini import GeminiProvider

        # Should work with OpenAI API strategy
        gemini_openai = GeminiProvider(strategy=OpenAIAPIStrategy())
        assert gemini_openai.strategy is not None

        # Should work with native strategy
        gemini_native = GeminiProvider(strategy=GeminiNativeStrategy())
        assert gemini_native.strategy is not None

        # Both should have same interface
        assert hasattr(gemini_openai, 'get_client')
        assert hasattr(gemini_native, 'get_client')
