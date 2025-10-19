# Architecture Deep Dive

This document explains the architectural decisions and design patterns used in this project.

## Design Patterns

### 1. Strategy Pattern

**Intent**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Implementation in This Project**:

```
BaseStrategy (Interface)
├── OpenAIAPIStrategy    # For OpenAI-compatible APIs
└── GeminiNativeStrategy # For Google's native SDK
```

**Why This Pattern?**
- Different LLM providers have different APIs
- We want to switch between them without changing provider code
- Allows the same provider (Gemini) to use multiple API implementations

**Code Example**:
```python
# The strategy defines HOW to communicate with an API
class BaseStrategy(ABC):
    @abstractmethod
    def get_client(self, provider):
        pass
    
    @abstractmethod
    def summarize(self, provider, client, website_content, system_prompt, user_prompt_prefix):
        pass

# Provider uses the strategy
class GeminiProvider(BaseProvider):
    def __init__(self, strategy):  # Strategy is injected
        self.strategy = strategy
        
# You can now use different strategies
gemini_openai = GeminiProvider(OpenAIAPIStrategy())
gemini_native = GeminiProvider(GeminiNativeStrategy())
```

### 2. Template Method Pattern (Implicit)

**Intent**: Define the skeleton of an algorithm, letting subclasses override specific steps.

**Implementation**:
```python
# BaseProvider defines the template
class BaseProvider(ABC):
    def get_client(self):
        return self.strategy.get_client(self)  # Step 1: Get client
    
    def summarize(self, client, content, system_prompt, user_prompt):
        return self.strategy.summarize(...)    # Step 2: Generate summary

# Concrete providers just configure themselves
class OllamaProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            name="Ollama",
            model="llama3.2:latest",
            strategy=OpenAIAPIStrategy(),  # Different strategy
            # ... configuration
        )
```

### 3. Dependency Injection

**Intent**: Provide dependencies from the outside rather than creating them internally.

**Benefits**:
- **Testability**: Easy to inject mock strategies for testing
- **Flexibility**: Change behavior without modifying code
- **Loose Coupling**: Providers don't know about concrete strategies

**Example**:
```python
# ❌ BAD: Hard dependency
class GeminiProvider:
    def __init__(self):
        self.strategy = GeminiNativeStrategy()  # Tightly coupled!

# ✅ GOOD: Injected dependency
class GeminiProvider:
    def __init__(self, strategy):
        self.strategy = strategy  # Can inject ANY strategy
```

## Architectural Principles

### Single Responsibility Principle (SRP)

Each class has ONE reason to change:

| Class | Single Responsibility |
|-------|----------------------|
| `BaseProvider` | Define provider interface |
| `OllamaProvider` | Configure Ollama-specific settings |
| `BaseStrategy` | Define strategy interface |
| `OpenAIAPIStrategy` | Implement OpenAI API communication |
| `summarizer.py` | Orchestrate summarization workflow |
| `scraper.py` | Fetch website content |

### Open/Closed Principle (OCP)

**"Open for extension, closed for modification"**

Adding a new provider doesn't require changing existing code:

```python
# No need to modify BaseProvider or strategies!
class ClaudeProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            name="Claude",
            model="claude-3-5-sonnet-20241022",
            strategy=OpenAIAPIStrategy(),  # Reuse existing strategy
            # ...
        )
```

### Dependency Inversion Principle (DIP)

**"Depend on abstractions, not concretions"**

```python
# ✅ GOOD: Providers depend on BaseStrategy (abstraction)
class BaseProvider:
    def __init__(self, strategy: BaseStrategy):  # Not a concrete class
        self.strategy = strategy

# ✅ GOOD: Summarizer depends on BaseProvider (abstraction)
def summarize_and_display(provider: BaseProvider, url: str):
    client = provider.get_client()  # Not a specific provider
```

## Module Organization

### Why `providers/` and `strategies/` are Separate?

**Separation of Concerns**:
- `providers/` → "WHO are we talking to?" (Ollama, OpenAI, Gemini)
- `strategies/` → "HOW do we talk to them?" (OpenAI API, Native SDK)

**Benefits**:
- Clear mental model
- Easy to find code
- Strategies can be reused across providers

### Why `core/` Directory?

**Business Logic Isolation**:
- `core/summarizer.py` contains the application workflow
- If you change from web summarization to document Q&A, only `core/` changes
- Providers and strategies remain untouched

## Key Design Decisions

### 1. Where to Load Environment Variables?

**Decision**: In `base_provider.py`

**Alternatives Considered**:
- ❌ In main script → Creates coupling
- ❌ In each provider → Code duplication
- ✅ In base provider → DRY, encapsulated, runs once

**Reasoning**:
```python
# Loaded once when any provider is imported
# providers/base_provider.py
from dotenv import load_dotenv
load_dotenv(override=True)

class BaseProvider(ABC):
    # All providers inherit this
```

### 2. Strategy as Constructor Parameter vs Property?

**Decision**: Constructor parameter for Gemini, fixed for others

**Why?**
- Ollama and OpenAI only support one API style
- Gemini supports multiple APIs (OpenAI-compatible and native)
- Constructor injection gives maximum flexibility where needed

```python
# Fixed strategy (most providers)
class OllamaProvider(BaseProvider):
    def __init__(self):
        super().__init__(strategy=OpenAIAPIStrategy())  # Always this

# Flexible strategy (Gemini)
class GeminiProvider(BaseProvider):
    def __init__(self, strategy):  # User chooses
        super().__init__(strategy=strategy)
```

### 3. Why Not Use ABC for Providers?

**Decision**: `BaseProvider` is abstract, but concrete providers are not

**Reasoning**:
- Concrete providers (Ollama, OpenAI, Gemini) don't need to be subclassed
- They are **leaf nodes** in the inheritance tree
- Making them abstract would be over-engineering

### 4. Model Name Customization

**Decision**: Optional `model_name` parameter

**Why?**
- Provides sensible defaults (`llama3.2:latest`, `gpt-4o-mini`)
- Allows easy experimentation with different models
- Keeps configuration in one place (main script)

```python
# Use default
provider = OllamaProvider()

# Override model
provider = OllamaProvider(model_name="llama3.3:latest")
```

## Error Handling Strategy

### Current Approach: Graceful Degradation

```python
def summarize(self, provider, client, website_content, ...):
    try:
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with {provider.name}: {e}"
```

**Philosophy**: Don't crash the entire run if one provider fails

**Benefits**:
- Other providers still run
- User sees which provider failed
- Useful for comparing provider reliability

### Production Enhancement Ideas

For production use, consider:

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def summarize(self, provider, client, website_content, ...):
    try:
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    except RateLimitError as e:
        logger.warning(f"Rate limit hit for {provider.name}, retrying...")
        raise  # Retry
    except AuthenticationError as e:
        logger.error(f"Auth failed for {provider.name}: {e}")
        return f"Authentication error: {e}"  # Don't retry
    except Exception as e:
        logger.exception(f"Unexpected error with {provider.name}")
        raise  # Retry up to limit
```

## Extension Points

### Where Can You Extend This Architecture?

1. **New Providers** → Add to `providers/`
2. **New API Strategies** → Add to `providers/strategies/`
3. **New Use Cases** → Modify `core/summarizer.py`
4. **New Output Formats** → Modify `summarize_and_display()`
5. **New Input Sources** → Modify `scraper.py` or add alternatives

### Example: Adding Streaming Support

```python
# providers/strategies/base_strategy.py
class BaseStrategy(ABC):
    @abstractmethod
    def summarize_stream(self, provider, client, content, system_prompt, user_prompt):
        """Yield chunks of the response as they arrive."""
        pass

# providers/strategies/openai_api_strategy.py
def summarize_stream(self, provider, client, content, system_prompt, user_prompt):
    stream = client.chat.completions.create(
        model=provider.model,
        messages=[...],
        stream=True  # Enable streaming
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# core/summarizer.py
def summarize_and_display_stream(provider, url):
    # ... fetch content ...
    console.print(f"[cyan]{provider.name}[/cyan]")
    for chunk in provider.strategy.summarize_stream(...):
        console.print(chunk, end="")
```

## Testing Strategy

### Unit Tests

```python
# tests/test_providers.py
from unittest.mock import Mock
from providers.ollama import OllamaProvider
from providers.strategies.openai_api_strategy import OpenAIAPIStrategy

def test_ollama_provider_initialization():
    provider = OllamaProvider()
    assert provider.name == "Ollama"
    assert provider.model == "llama3.2:latest"
    assert isinstance(provider.strategy, OpenAIAPIStrategy)

def test_custom_model():
    provider = OllamaProvider(model_name="custom-model")
    assert provider.model == "custom-model"
```

### Integration Tests

```python
# tests/test_integration.py
def test_summarization_workflow():
    # Use a mock strategy to avoid API calls
    mock_strategy = Mock()
    mock_strategy.get_client.return_value = Mock()
    mock_strategy.summarize.return_value = "Test summary"
    
    provider = GeminiProvider(strategy=mock_strategy)
    # ... test summarize_and_display ...
```

## Performance Considerations

### Current Design: Sequential Processing

```python
for provider in PROVIDERS:
    summarize_and_display(provider, target_url)  # One at a time
```

**Pros**: Simple, easy to debug
**Cons**: Slow for multiple providers

### Async Enhancement

```python
import asyncio

async def summarize_async(provider, url):
    # Async version of summarize_and_display
    pass

async def main():
    tasks = [summarize_async(provider, url) for provider in PROVIDERS]
    await asyncio.gather(*tasks)  # Run in parallel

if __name__ == "__main__":
    asyncio.run(main())
```

**Benefits**: 3x faster with 3 providers

## Scalability Considerations

### Current: Single URL, Multiple Providers
**Use Case**: Compare how different LLMs summarize the same content

### Future: Multiple URLs, Multiple Providers
**Architecture Enhancement**:

```python
# Batch processing
URLS = ["https://example.com", "https://example2.com", ...]
PROVIDERS = [OllamaProvider(), OpenAIProvider(), ...]

for url in URLS:
    for provider in PROVIDERS:
        summarize_and_display(provider, url)
        # Or use async for parallel processing
```

## Conclusion

This architecture demonstrates:
- ✅ Professional software design patterns
- ✅ SOLID principles in practice
- ✅ Clean, maintainable code organization
- ✅ Easy extensibility for new features

It serves as a **template** for building LLM-powered applications with multiple providers and flexible API integrations.
