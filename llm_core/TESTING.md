# Testing Guide for LLM Playground

This document explains the testing strategy and best practices used in this project.

## 🎯 Philosophy

> "Tests are not just about catching bugs—they're about documenting behavior and enabling confident changes."

Our testing approach:
- **Fast by default** - Unit tests with mocks run in milliseconds
- **Reliable** - Tests don't depend on external services
- **Educational** - Tests demonstrate how to use the code
- **Practical** - Tests catch real issues

## 📁 Test Structure

```
llm_core/tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── test_providers.py              # Provider unit tests
└── test_strategies.py             # Strategy unit tests

applications/summarize_webpage/tests/
├── __init__.py
├── conftest.py                    # App-specific fixtures
├── test_scraper.py                # Scraping tests
└── test_summarizer.py             # Workflow tests
```

## 🚀 Running Tests

### Install Test Dependencies

```bash
# Install llm_core with dev dependencies
cd llm_core
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Run All Tests

```bash
# From project root
pytest

# With coverage report
pytest --cov=llm_core --cov-report=html

# With verbose output
pytest -v
```

### Run Specific Test Categories

```bash
# Only unit tests (fast, no external dependencies)
pytest -m unit

# Only integration tests (slow, requires API keys)
pytest -m integration

# Skip integration tests (recommended for CI)
pytest -m "not integration"

# Run tests for a specific module
pytest llm_core/tests/test_providers.py

# Run a specific test
pytest llm_core/tests/test_providers.py::TestProviderInitialization::test_ollama_default_initialization
```

## 📊 Test Categories

### Unit Tests (`@pytest.mark.unit`)

**Purpose**: Test individual components in isolation

**Characteristics**:
- ✅ Fast (< 1 second total)
- ✅ No network calls
- ✅ Use mocks for external dependencies
- ✅ Deterministic (same input → same output)

**Example**:
```python
@pytest.mark.unit
def test_provider_initialization():
    provider = OpenAIProvider(model_name="gpt-4o-mini")
    assert provider.model == "gpt-4o-mini"
```

### Integration Tests (`@pytest.mark.integration`)

**Purpose**: Test interactions with real external services

**Characteristics**:
- ⚠️ Slow (API latency)
- ⚠️ Requires API keys
- ⚠️ May cost money
- ⚠️ Can be flaky (network issues)

**Example**:
```python
@pytest.mark.integration
@pytest.mark.slow
def test_openai_real_api(skip_if_no_api_keys):
    skip_if_no_api_keys("openai")
    provider = OpenAIProvider()
    # ... make real API call ...
```

## 🎓 Best Practices Demonstrated

### 1. Use Fixtures for Reusable Setup

**Bad** ❌:
```python
def test_one():
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = Mock()
    # ... test logic ...

def test_two():
    mock_client = Mock()  # Duplicate setup!
    mock_client.chat.completions.create.return_value = Mock()
    # ... test logic ...
```

**Good** ✅:
```python
@pytest.fixture
def mock_openai_client():
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = Mock()
    return mock_client

def test_one(mock_openai_client):
    # Use fixture
    
def test_two(mock_openai_client):
    # Reuse same setup
```

### 2. Parametrize Tests for Multiple Cases

**Bad** ❌:
```python
def test_ollama_custom_model():
    provider = OllamaProvider(model_name="model1")
    assert provider.model == "model1"

def test_ollama_another_model():
    provider = OllamaProvider(model_name="model2")
    assert provider.model == "model2"
```

**Good** ✅:
```python
@pytest.mark.parametrize("model_name", [
    "model1",
    "model2",
    "model3",
])
def test_ollama_custom_models(model_name):
    provider = OllamaProvider(model_name=model_name)
    assert provider.model == model_name
```

### 3. Test the Interface, Not the Implementation

**Bad** ❌:
```python
def test_provider_internal_attribute():
    provider = OpenAIProvider()
    assert provider._internal_cache == {}  # Testing implementation detail
```

**Good** ✅:
```python
def test_provider_interface():
    provider = OpenAIProvider()
    assert hasattr(provider, 'get_client')
    assert hasattr(provider, 'summarize')
    assert callable(provider.summarize)  # Test public interface
```

### 4. Mock External Dependencies

**Bad** ❌:
```python
def test_summarization():
    provider = OpenAIProvider()
    result = provider.summarize(...)  # Makes real API call!
```

**Good** ✅:
```python
def test_summarization(mock_openai_client):
    provider = OpenAIProvider()
    result = provider.summarize(client=mock_openai_client, ...)  # Uses mock
```

### 5. Test Error Handling

```python
def test_handles_api_error(mock_openai_client):
    # Configure mock to raise exception
    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
    
    provider = OpenAIProvider()
    result = provider.summarize(client=mock_openai_client, ...)
    
    # Should handle gracefully, not crash
    assert "error" in result.lower()
```

### 6. Use Descriptive Test Names

**Bad** ❌:
```python
def test_1():
    ...

def test_provider():
    ...
```

**Good** ✅:
```python
def test_ollama_uses_default_model_when_none_specified():
    ...

def test_provider_handles_missing_api_key_gracefully():
    ...
```

## 🔧 Common Commands

```bash
# Run tests with output
pytest -v

# Run tests with print statements
pytest -s

# Run specific test file
pytest llm_core/tests/test_providers.py

# Run tests matching a pattern
pytest -k "test_openai"

# Run with coverage
pytest --cov=llm_core --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=llm_core --cov-report=html
open htmlcov/index.html
```

## 📚 Learning Resources

### Pytest Documentation
- [Official Pytest Docs](https://docs.pytest.org/)
- [Fixtures Guide](https://docs.pytest.org/en/stable/fixture.html)
- [Parametrization](https://docs.pytest.org/en/stable/parametrize.html)

### Testing Best Practices
- [Testing Best Practices (Real Python)](https://realpython.com/pytest-python-testing/)
- [Effective Python Testing](https://effectivepython.com/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## ✅ Summary

**Key Takeaways**:
1. ✅ Write unit tests first (fast, reliable)
2. ✅ Use fixtures to DRY up test setup
3. ✅ Mock external dependencies (APIs, databases)
4. ✅ Test behavior, not implementation
5. ✅ Use integration tests sparingly (slow, expensive)
6. ✅ Organize tests into clear categories
7. ✅ Aim for meaningful coverage, not 100%

**Remember**: Good tests make refactoring safe and documentation clear!
