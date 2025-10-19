"""
Tests for web scraping functionality.

These tests demonstrate:
- Mocking browser automation (Playwright)
- Testing HTML parsing (BeautifulSoup)
- Isolating network-dependent code
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from scraper import fetch_website_contents


@pytest.mark.unit
class TestWebscraper:
    """Test web scraping logic."""

    @patch('scraper.sync_playwright')
    def test_fetch_website_contents_with_mock(self, mock_playwright):
        """Test scraping with mocked Playwright browser."""
        # Setup the mock to return proper HTML string
        mock_page = MagicMock()
        mock_page.content.return_value = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Website</h1>
                <p>This is test content.</p>
                <script>console.log('ignored');</script>
            </body>
        </html>
        """

        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page

        mock_playwright_ctx = MagicMock()
        mock_playwright_ctx.chromium.launch.return_value = mock_browser

        mock_playwright.return_value.__enter__.return_value = mock_playwright_ctx

        url = "https://example.com"
        content = fetch_website_contents(url)

        # Should return cleaned text content
        assert isinstance(content, str)
        assert len(content) > 0
        assert "Test Website" in content
        assert "test content" in content.lower()

        # Scripts should be removed
        assert "console.log" not in content

    @patch('scraper.sync_playwright')
    def test_fetch_website_removes_scripts_and_styles(self, mock_playwright):
        """Verify that scripts and styles are removed from content."""
        mock_page = MagicMock()
        mock_page.content.return_value = """
        <html>
            <head>
                <style>.test { color: red; }</style>
            </head>
            <body>
                <p>Content</p>
                <script>alert('test');</script>
            </body>
        </html>
        """

        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page

        mock_playwright_ctx = MagicMock()
        mock_playwright_ctx.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_ctx

        content = fetch_website_contents("https://example.com")

        # These should NOT appear in the cleaned content
        assert "alert" not in content
        assert ".test" not in content
        assert "color: red" not in content

    @patch('scraper.sync_playwright')
    def test_fetch_website_handles_errors_gracefully(self, mock_playwright):
        """Test error handling when scraping fails."""
        # Simulate an error
        mock_playwright.side_effect = Exception("Network error")

        result = fetch_website_contents("https://example.com")

        # Should return error message, not crash
        assert "Error" in result
        assert "Network error" in result

    @pytest.mark.integration
    def test_fetch_real_website(self):
        """
        Integration test: Fetch a real website.

        This is marked as integration and slow.
        Run with: pytest -m integration
        """
        # Use a reliable, fast website
        content = fetch_website_contents("https://example.com")

        assert isinstance(content, str)
        assert len(content) > 0
        # example.com has predictable content
        assert "example" in content.lower()


@pytest.mark.unit
class TestHTMLCleaning:
    """Test HTML cleaning and text extraction logic."""

    @patch('scraper.sync_playwright')
    def test_removes_empty_lines(self, mock_playwright):
        """Cleaned content should not have excessive whitespace."""
        mock_page = MagicMock()
        mock_page.content.return_value = """
        <html>
            <body>
                <p>Line 1</p>


                <p>Line 2</p>
            </body>
        </html>
        """

        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page

        mock_playwright_ctx = MagicMock()
        mock_playwright_ctx.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_ctx

        content = fetch_website_contents("https://example.com")

        # Should not have multiple consecutive newlines
        assert "\n\n\n" not in content

    @patch('scraper.sync_playwright')
    def test_preserves_meaningful_content(self, mock_playwright):
        """Important content should be preserved."""
        mock_page = MagicMock()
        mock_page.content.return_value = """
        <html>
            <body>
                <h1>Test Website</h1>
                <p>This is test content.</p>
            </body>
        </html>
        """

        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page

        mock_playwright_ctx = MagicMock()
        mock_playwright_ctx.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_ctx

        content = fetch_website_contents("https://example.com")

        # Headings and paragraphs should be in the result
        assert "Test Website" in content
        assert "test content" in content.lower()
