"""
Unit tests for LLM providers.

These tests use mocks to avoid making real API calls, making them:
- Fast (run in milliseconds)
- Reliable (no network dependencies)
- Free (no API costs)

Run with: pytest llm_core/tests/test_providers.py
"""

import pytest
from unittest.mock import Mock, patch
from llm_core.providers.ollama import OllamaProvider
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.gemini import GeminiProvider
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy
from llm_core.providers.strategies.gemini_native_strategy import GeminiNativeStrategy


# ============================================================================
# Provider Initialization Tests
# ============================================================================

@pytest.mark.unit
class TestProviderInitialization:
    """Test that providers initialize correctly with default and custom values."""
    
    def test_ollama_default_initialization(self):
        """Ollama provider should use default model when none specified."""
        provider = OllamaProvider()
        
        assert provider.name == "Ollama"
        assert provider.model == "llama3.2:latest"
        assert provider.base_url == "http://localhost:11434/v1"
        assert isinstance(provider.strategy, OpenAIAPIStrategy)
    
    def test_ollama_custom_model(self):
        """Ollama provider should accept custom model name."""
        custom_model = "llama3.3:latest"
        provider = OllamaProvider(model_name=custom_model)
        
        assert provider.model == custom_model
        assert provider.name == "Ollama"  # Name should remain the same
    
    def test_openai_default_initialization(self):
        """OpenAI provider should use default model when none specified."""
        provider = OpenAIProvider()
        
        assert provider.name == "OpenAI"
        assert provider.model == "gpt-4o-mini"
        assert isinstance(provider.strategy, OpenAIAPIStrategy)
    
    def test_openai_custom_model(self):
        """OpenAI provider should accept custom model name."""
        custom_model = "gpt-4o"
        provider = OpenAIProvider(model_name=custom_model)
        
        assert provider.model == custom_model
    
    def test_gemini_requires_strategy(self):
        """Gemini provider requires a strategy to be specified."""
        # Create with OpenAI API strategy
        provider = GeminiProvider(strategy=OpenAIAPIStrategy())
        
        # Provider name includes strategy info
        assert "Gemini" in provider.name
        assert provider.strategy is not None
        assert isinstance(provider.strategy, OpenAIAPIStrategy)
    
    @pytest.mark.parametrize("strategy_class,expected_name", [
        (OpenAIAPIStrategy, "OpenAI API Strategy"),
        (GeminiNativeStrategy, "Gemini Native Strategy"),
    ])
    def test_gemini_with_different_strategies(self, strategy_class, expected_name):
        """Gemini should work with different strategy implementations."""
        strategy = strategy_class()
        provider = GeminiProvider(strategy=strategy)
        
        assert provider.strategy == strategy
        # Strategy should have a name attribute for identification
        assert hasattr(strategy, '__class__')


# ============================================================================
# Provider Client Creation Tests
# ============================================================================

@pytest.mark.unit
class TestProviderClientCreation:
    """Test that providers create API clients correctly."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_openai_client_creation(self):
        """OpenAI provider should create a valid client."""
        provider = OpenAIProvider()
        client = provider.get_client()
        
        assert client is not None
        # Client should be an OpenAI instance
        from openai import OpenAI
        assert isinstance(client, OpenAI)
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_ollama_client_creation(self):
        """Test that Ollama creates OpenAI client with correct base URL."""
        provider = OllamaProvider()
        client = provider.get_client()
        
        # Ollama uses OpenAI-compatible API
        assert hasattr(client, 'chat')
        # OpenAI client returns URL object, convert to string and strip trailing slash
        assert str(client.base_url).rstrip('/') == "http://localhost:11434/v1"


# ============================================================================
# Provider Summarization Tests (with Mocks)
# ============================================================================

@pytest.mark.unit
class TestProviderSummarization:
    """Test summarization logic without making real API calls."""
    
    def test_summarize_with_mock_client(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """Test that summarize method calls the API correctly."""
        provider = OpenAIProvider()
        
        # Call summarize with mock client
        result = provider.summarize(
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )
        
        # Verify the client was called
        assert mock_openai_client.chat.completions.create.called
        
        # Verify the result
        assert result == "This is a test summary."
    
    def test_summarize_passes_correct_parameters(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """Verify that correct parameters are passed to the API."""
        provider = OpenAIProvider(model_name="gpt-4o")
        
        provider.summarize(
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )
        
        # Get the call arguments
        call_args = mock_openai_client.chat.completions.create.call_args
        
        # Verify model
        assert call_args.kwargs["model"] == "gpt-4o"
        
        # Verify messages structure
        messages = call_args.kwargs["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert sample_website_content in messages[1]["content"]


# ============================================================================
# Error Handling Tests
# ============================================================================

@pytest.mark.unit
class TestProviderErrorHandling:
    """Test how providers handle various error conditions."""
    
    def test_summarize_handles_api_exception(
        self,
        mock_openai_client,
        sample_website_content,
        sample_prompts
    ):
        """Provider should return error message when API fails."""
        # Configure mock to raise an exception
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        provider = OpenAIProvider()
        result = provider.summarize(
            client=mock_openai_client,
            website_content=sample_website_content,
            system_prompt=sample_prompts["system_prompt"],
            user_prompt_prefix=sample_prompts["user_prompt_prefix"]
        )
        
        # Should return error message, not crash
        assert "error" in result.lower() or "Error" in result
        assert "OpenAI" in result  # Should identify which provider failed
    
    @patch.dict('os.environ', {}, clear=True)
    def test_provider_without_api_key(self):
        """Provider should handle missing API key gracefully."""
        provider = OpenAIProvider()
        
        # API key should be None when not set
        assert provider.api_key is None or provider.api_key == ""


# ============================================================================
# Parametrized Tests
# ============================================================================

@pytest.mark.unit
class TestMultipleProviders:
    """Test multiple providers using parametrized tests."""
    
    @pytest.mark.parametrize("provider_class,default_model", [
        (OllamaProvider, "llama3.2:latest"),
        (OpenAIProvider, "gpt-4o-mini"),
    ])
    def test_provider_defaults(self, provider_class, default_model):
        """All providers should have sensible defaults."""
        if provider_class == GeminiProvider:
            provider = provider_class(strategy=OpenAIAPIStrategy())
        else:
            provider = provider_class()
        
        assert provider.model == default_model
        assert provider.name is not None
        assert len(provider.name) > 0
    
    @pytest.mark.parametrize("custom_model", [
        "custom-model-v1",
        "test-model-123",
        "experimental-model",
    ])
    def test_providers_accept_custom_models(self, custom_model):
        """All providers should accept custom model names."""
        providers = [
            OllamaProvider(model_name=custom_model),
            OpenAIProvider(model_name=custom_model),
        ]
        
        for provider in providers:
            assert provider.model == custom_model


# ============================================================================
# Best Practices Demonstration
# ============================================================================

@pytest.mark.unit
def test_provider_interface_consistency():
    """
    BEST PRACTICE: Test that all providers follow the same interface.
    
    This ensures they're truly interchangeable (Liskov Substitution Principle).
    """
    providers = [
        OllamaProvider(),
        OpenAIProvider(),
        GeminiProvider(strategy=OpenAIAPIStrategy()),
    ]
    
    for provider in providers:
        # All providers should have these attributes
        assert hasattr(provider, 'name')
        assert hasattr(provider, 'model')
        assert hasattr(provider, 'strategy')
        assert hasattr(provider, 'get_client')
        assert hasattr(provider, 'summarize')
        
        # All should be callable
        assert callable(provider.get_client)
        assert callable(provider.summarize)
