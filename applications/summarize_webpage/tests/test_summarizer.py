"""
Tests for summarization workflow orchestration.

These tests demonstrate:
- Testing business logic
- Mocking multiple dependencies
- Testing Rich console output
- Testing workflow integration
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
from core.summarizer import summarize_and_display, system_prompt, user_prompt_prefix


@pytest.mark.unit
class TestSummarizationWorkflow:
    """Test the end-to-end summarization workflow."""

    @patch('core.summarizer.fetch_website_contents')
    @patch('core.summarizer.console')
    def test_summarize_and_display_success(
        self,
        mock_console,
        mock_fetch,
        mock_openai_client,
        sample_website_content
    ):
        """Test successful summarization workflow."""
        # Set up mocks
        mock_fetch.return_value = sample_website_content

        # Create a mock provider
        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        mock_provider.model = "test-model"
        mock_provider.api_key = "test-key"
        mock_provider.get_client.return_value = mock_openai_client
        mock_provider.summarize.return_value = "This is a summary."

        # Run the workflow
        url = "https://example.com"
        summarize_and_display(mock_provider, url)

        # Verify the workflow
        mock_fetch.assert_called_once_with(url)
        mock_provider.get_client.assert_called_once()
        mock_provider.summarize.assert_called_once_with(
            mock_openai_client,
            sample_website_content,
            system_prompt,
            user_prompt_prefix
        )

        # Verify console output was called
        assert mock_console.print.called

    @patch('core.summarizer.console')
    def test_summarize_without_api_key(self, mock_console):
        """Test that workflow handles missing API key gracefully."""
        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        mock_provider.api_key = None  # No API key

        summarize_and_display(mock_provider, "https://example.com")

        # Should print error message
        assert mock_console.print.called
        # Should NOT call get_client or summarize
        assert not mock_provider.get_client.called

    @patch('core.summarizer.fetch_website_contents')
    @patch('core.summarizer.console')
    def test_summarize_handles_scraping_error(
        self,
        mock_console,
        mock_fetch
    ):
        """Test workflow when web scraping fails."""
        # Simulate scraping error
        mock_fetch.return_value = "Error fetching website content: Network timeout"

        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        mock_provider.api_key = "test-key"

        summarize_and_display(mock_provider, "https://example.com")

        # Should print error, not call LLM
        assert mock_console.print.called
        assert not mock_provider.summarize.called


@pytest.mark.unit
class TestPromptConfiguration:
    """Test that prompts are configured correctly."""

    def test_system_prompt_exists(self):
        """System prompt should be defined and non-empty."""
        assert system_prompt is not None
        assert len(system_prompt) > 0
        assert isinstance(system_prompt, str)

    def test_user_prompt_prefix_exists(self):
        """User prompt prefix should be defined."""
        assert user_prompt_prefix is not None
        assert len(user_prompt_prefix) > 0
        assert isinstance(user_prompt_prefix, str)

    def test_prompts_have_instructions(self):
        """Prompts should contain actual instructions."""
        # System prompt should describe behavior
        assert any(word in system_prompt.lower() for word in [
            "you are", "assistant", "summarize", "analyze"
        ])

        # User prompt should have instructions
        assert any(word in user_prompt_prefix.lower() for word in [
            "summarize", "content", "website"
        ])
