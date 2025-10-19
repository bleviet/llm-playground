"""
Tests for CLI (Command Line Interface) functionality.

These tests demonstrate:
- Testing Click commands
- Testing command-line arguments and options
- Input validation
- Provider selection logic
"""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from summarize_webpage import main, PROVIDERS


@pytest.mark.unit
class TestCLIArguments:
    """Test command-line argument parsing."""
    
    def test_cli_with_default_url(self):
        """Test CLI with no arguments uses default URL."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, [])
            
            # Should use default URL
            assert result.exit_code == 0
            assert mock_summarize.call_count == len(PROVIDERS)
            
            # Check that default URL was used
            first_call = mock_summarize.call_args_list[0]
            assert 'anthropic.com' in first_call[0][1]
    
    def test_cli_with_custom_url(self):
        """Test CLI with custom URL argument."""
        runner = CliRunner()
        custom_url = "https://www.python.org"
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, [custom_url])
            
            assert result.exit_code == 0
            
            # Check that custom URL was passed to all providers
            for call in mock_summarize.call_args_list:
                assert call[0][1] == custom_url
    
    def test_cli_rejects_invalid_url(self):
        """Test that invalid URLs are rejected."""
        runner = CliRunner()
        invalid_urls = [
            "not-a-url",
            "www.example.com",  # Missing protocol
            "ftp://example.com",  # Wrong protocol
        ]
        
        for invalid_url in invalid_urls:
            with patch('summarize_webpage.summarize_and_display') as mock_summarize:
                result = runner.invoke(main, [invalid_url])
                
                # Should fail validation
                assert result.exit_code != 0
                assert "Invalid URL" in result.output
                # Should not call summarize
                assert mock_summarize.call_count == 0


@pytest.mark.unit
class TestProviderSelection:
    """Test provider selection via CLI options."""
    
    def test_select_single_provider_ollama(self):
        """Test selecting only Ollama provider."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '--provider', 'ollama'])
            
            assert result.exit_code == 0
            # Should only call once (for Ollama)
            assert mock_summarize.call_count == 1
            
            # Check it's the Ollama provider
            provider = mock_summarize.call_args[0][0]
            assert 'Ollama' in provider.name
    
    def test_select_single_provider_openai(self):
        """Test selecting only OpenAI provider."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '--provider', 'openai'])
            
            assert result.exit_code == 0
            assert mock_summarize.call_count == 1
            
            provider = mock_summarize.call_args[0][0]
            assert 'OpenAI' in provider.name
    
    def test_select_gemini_openai_strategy(self):
        """Test selecting Gemini with OpenAI API strategy."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '--provider', 'gemini-openai'])
            
            assert result.exit_code == 0
            assert mock_summarize.call_count == 1
            
            provider = mock_summarize.call_args[0][0]
            assert 'Gemini' in provider.name
            assert 'OpenAI' in provider.name  # OpenAI API strategy
    
    def test_select_gemini_native_strategy(self):
        """Test selecting Gemini with native strategy."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '--provider', 'gemini-native'])
            
            assert result.exit_code == 0
            assert mock_summarize.call_count == 1
            
            provider = mock_summarize.call_args[0][0]
            assert 'Gemini' in provider.name
            assert 'Native' in provider.name  # Native strategy
    
    def test_select_all_providers(self):
        """Test selecting all providers (default behavior)."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '--provider', 'all'])
            
            assert result.exit_code == 0
            # Should call for all 4 providers
            assert mock_summarize.call_count == len(PROVIDERS)
    
    def test_provider_short_option(self):
        """Test using -p short option for provider selection."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            result = runner.invoke(main, ['https://example.com', '-p', 'openai'])
            
            assert result.exit_code == 0
            assert mock_summarize.call_count == 1


@pytest.mark.unit
class TestCLIOutput:
    """Test CLI output formatting."""
    
    def test_cli_shows_url_being_summarized(self):
        """Test that CLI displays the URL being processed."""
        runner = CliRunner()
        test_url = "https://www.example.com"
        
        with patch('summarize_webpage.summarize_and_display'):
            result = runner.invoke(main, [test_url])
            
            assert result.exit_code == 0
            assert test_url in result.output
            assert "Summarizing" in result.output
    
    def test_cli_shows_provider_count(self):
        """Test that CLI shows how many providers will be used."""
        runner = CliRunner()
        
        with patch('summarize_webpage.summarize_and_display'):
            # All providers
            result = runner.invoke(main, ['https://example.com', '-p', 'all'])
            assert "4 provider(s)" in result.output
            
            # Single provider
            result = runner.invoke(main, ['https://example.com', '-p', 'openai'])
            assert "1 provider(s)" in result.output


@pytest.mark.unit
class TestCLIHelp:
    """Test CLI help functionality."""
    
    def test_help_option(self):
        """Test --help option displays usage information."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Summarize a webpage" in result.output
        assert "URL" in result.output
        assert "--provider" in result.output
        assert "Examples:" in result.output
    
    def test_help_shows_provider_choices(self):
        """Test that help shows all provider choices."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        # Should list all available providers
        assert "ollama" in result.output.lower()
        assert "openai" in result.output.lower()
        assert "gemini" in result.output.lower()


@pytest.mark.integration
class TestCLIIntegration:
    """Integration tests for full CLI workflow."""
    
    def test_full_workflow_with_mock(self):
        """Test complete workflow from CLI to summarization."""
        runner = CliRunner()
        
        # Create mock provider with required attributes
        mock_provider = Mock()
        mock_provider.name = "TestProvider"
        
        with patch('summarize_webpage.summarize_and_display') as mock_summarize:
            with patch('summarize_webpage.PROVIDERS', [mock_provider] * 4):  # 4 providers for 'all'
                result = runner.invoke(main, [
                    'https://www.python.org',
                    '--provider', 'all'
                ])
                
                assert result.exit_code == 0
                assert mock_summarize.call_count == 4
