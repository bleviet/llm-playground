"""
Pytest configuration and shared fixtures for llm_core tests.

Fixtures are reusable test components that:
- Set up test data
- Provide mock objects
- Configure test environment
- Clean up after tests

Read more: https://docs.pytest.org/en/stable/fixture.html
"""

import os
import pytest
from unittest.mock import Mock, MagicMock


# ============================================================================
# Environment Setup Fixtures
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Set up test environment variables before any tests run.

    Scope: session - Runs once per test session
    Autouse: True - Runs automatically without being requested
    """
    # Save original env vars
    original_env = os.environ.copy()

    # Set test API keys (these will be overridden in specific tests)
    os.environ["OPENAI_API_KEY"] = "test-openai-key"
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"

    yield  # Tests run here

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# ============================================================================
# Mock Provider Fixtures
# ============================================================================

@pytest.fixture
def mock_openai_client():
    """
    Creates a mock OpenAI client for testing without API calls.

    Usage in tests:
        def test_something(mock_openai_client):
            # mock_openai_client is already configured
            response = mock_openai_client.chat.completions.create(...)
    """
    mock_client = MagicMock()

    # Configure the mock response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "This is a test summary."

    # Set up the mock method chain
    mock_client.chat.completions.create.return_value = mock_response

    return mock_client


@pytest.fixture
def mock_gemini_client():
    """
    Creates a mock Gemini client for testing without API calls.
    """
    mock_client = MagicMock()

    # Configure the mock response
    mock_response = Mock()
    mock_response.text = "This is a test Gemini summary."

    mock_client.generate_content.return_value = mock_response

    return mock_client


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_website_content():
    """
    Provides sample website content for testing.

    This avoids hardcoding test data in multiple places.
    """
    return """
    Welcome to Example Website

    This is a sample website with some content.
    It has multiple paragraphs and sections.

    About Us
    We are a company that does things.

    Contact
    Email: test@example.com
    """


@pytest.fixture
def sample_prompts():
    """
    Provides standard test prompts.
    """
    return {
        "system_prompt": "You are a helpful assistant that summarizes text.",
        "user_prompt_prefix": "Please summarize the following content:\n\n"
    }


# ============================================================================
# Provider Configuration Fixtures
# ============================================================================

@pytest.fixture
def provider_config():
    """
    Provides common provider configuration for testing.
    """
    return {
        "name": "TestProvider",
        "model": "test-model-v1",
        "api_key": "test-api-key-12345"
    }


# ============================================================================
# Parametrized Test Data
# ============================================================================

def pytest_configure(config):
    """
    Register custom markers for test categorization.

    Usage:
        @pytest.mark.unit
        @pytest.mark.integration
        @pytest.mark.slow
    """
    config.addinivalue_line("markers", "unit: Unit tests (fast, no external calls)")
    config.addinivalue_line("markers", "integration: Integration tests (requires API keys)")
    config.addinivalue_line("markers", "slow: Slow tests that may take time")


# ============================================================================
# Helper Functions
# ============================================================================

@pytest.fixture
def assert_valid_summary():
    """
    Provides a reusable assertion function for validating summaries.

    Usage:
        def test_something(assert_valid_summary):
            summary = generate_summary()
            assert_valid_summary(summary)
    """
    def _assert(summary: str):
        """Assert that a summary meets basic quality criteria."""
        assert isinstance(summary, str), "Summary should be a string"
        assert len(summary) > 0, "Summary should not be empty"
        assert len(summary) < 10000, "Summary should not be excessively long"
        assert not summary.startswith("Error"), "Summary should not be an error message"

    return _assert
