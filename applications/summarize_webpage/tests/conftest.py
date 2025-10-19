"""
Pytest configuration for summarize_webpage application tests.
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()

    mock_message.content = "This is a test summary."
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]

    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.text = "This is a test summary from Gemini."

    mock_client.generate_content.return_value = mock_response
    return mock_client


@pytest.fixture
def sample_website_content():
    """Sample website content for testing."""
    return """
    About Python

    Python is a programming language that lets you work quickly
    and integrate systems more effectively.

    Latest News
    - Python 3.12 Released
    - New Features in Python
    """



@pytest.fixture
def sample_html_content():
    """Provides sample HTML for scraper testing."""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Sample Website</title>
            <script>var x = 1;</script>
            <style>.test { color: red; }</style>
        </head>
        <body>
            <nav>Navigation Menu</nav>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content of the page.</p>
                <p>It has multiple paragraphs.</p>
            </main>
            <footer>Copyright 2024</footer>
        </body>
    </html>
    """
