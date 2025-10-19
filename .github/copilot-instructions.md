# GitHub Copilot Instructions

This file provides context for GitHub Copilot when working in this repository.

## Repository Context

This is a **learning-focused LLM playground** repository. Every project demonstrates professional software architecture patterns for working with Large Language Models.

## Code Generation Guidelines

### Architecture Patterns

When generating code, follow these patterns already established in the repo:

1. **Strategy Pattern** - See `summarize_webpage/providers/strategies/`
   - Separate WHAT (providers) from HOW (strategies)
   - Example: `OpenAIAPIStrategy`

2. **Provider Pattern** - See `summarize_webpage/providers/`
   - Abstract base class: `BaseProvider`
   - Concrete implementations: `OllamaProvider`, `OpenAIProvider`

3. **Dependency Injection** - Inject strategies into providers:
   ```python
   # Good pattern already in use
   provider = GeminiProvider(strategy=OpenAIAPIStrategy())
   ```

### Code Style

- **Python Version**: 3.11+ (see `.editorconfig`)
- **Formatting**: Black with 100 char line length
- **Type Hints**: Use for public APIs
- **Docstrings**: Required for all public classes and functions

### Documentation

Every new feature needs:
- Comments explaining WHY, not WHAT
- Docstrings with examples
- Updates to relevant markdown files

### File Structure

When creating new files, follow this structure:

```
project_name/
├── core/              # Business logic
├── providers/         # External integrations
│   └── strategies/   # API strategies
├── utils/            # Helper functions
└── tests/            # Test files
```

### Environment Variables

- Load via `python-dotenv` in base classes
- Document in `.env.example`
- Never hardcode API keys
- See `summarize_webpage/providers/base_provider.py` for the pattern

## Specific Instructions

### When suggesting new providers:

1. Create provider class inheriting from `BaseProvider`
2. Choose or create appropriate strategy
3. Add to `.env.example`
4. Update README and QUICKSTART
5. Include usage example

Example structure:
```python
from .base_provider import BaseProvider
from .strategies.openai_api_strategy import OpenAIAPIStrategy

class NewProvider(BaseProvider):
    def __init__(self, model_name=None):
        super().__init__(
            name="Provider Name",
            model=model_name or "default-model",
            strategy=OpenAIAPIStrategy(),
            api_key=os.getenv("PROVIDER_API_KEY")
        )
```

### When suggesting new strategies:

1. Inherit from `BaseStrategy`
2. Implement `get_client()` and `summarize()`
3. Handle errors gracefully
4. Document API-specific quirks

Example structure:
```python
from .base_strategy import BaseStrategy

class NewStrategy(BaseStrategy):
    def get_client(self, provider):
        # Create API client
        pass
    
    def summarize(self, provider, client, content, system_prompt, user_prompt):
        try:
            # API call
            pass
        except Exception as e:
            return f"Error with {provider.name}: {e}"
```

### When suggesting e rror handling:

Follow the graceful degradation pattern from `summarize_webpage/core/summarizer.py`:

```python
try:
    result = operation()
    return result
except SpecificError as e:
    console.print(f"Error: {e}", style="red")
    return None
```

### When suggesting imports:

Organize imports following this order:
1. Standard library
2. Third-party packages
3. Local modules

```python
import os
import logging

from openai import OpenAI
from rich.console import Console

from .base_provider import BaseProvider
```

## Common Tasks

### Adding a new LLM provider:

1. Check if `OpenAIAPIStrategy` works (most providers support it)
2. If not, create custom strategy in `providers/strategies/`
3. Create provider class in `providers/`
4. Add to `PROVIDERS` list in main script
5. Update documentation

### Modifying prompts:

Edit `summarize_webpage/core/summarizer.py`:
- `system_prompt` - How the LLM should behave
- `user_prompt_prefix` - Instructions for the specific task

### Changing web scraping:

Edit `summarize_webpage/scraper.py`:
- Uses Playwright for JavaScript rendering
- BeautifulSoup for parsing
- Returns clean text content

## Quality Checklist

Before generating code, ensure:

- [ ] Follows Strategy or Provider pattern where applicable
- [ ] Includes type hints for public APIs
- [ ] Has docstrings with examples
- [ ] Handles errors gracefully
- [ ] Uses dependency injection
- [ ] Respects SOLID principles
- [ ] Matches existing code style
- [ ] Includes usage example

## What NOT to suggest:

❌ Hardcoding API keys
❌ Creating god objects (classes doing too much)
❌ Breaking established patterns
❌ Over-engineering simple features
❌ Removing educational comments
❌ Using print() instead of logging/rich
❌ Tight coupling between components

## What TO suggest:

✅ Following existing patterns
✅ Improving documentation
✅ Adding type hints
✅ Extracting reusable components
✅ Simplifying complex code
✅ Adding error handling
✅ Improving test coverage

## Example Code Patterns

### Creating a provider with custom model:

```python
# This pattern is already established
provider = OpenAIProvider(model_name="gpt-4o")
provider = OllamaProvider(model_name="llama3.3:latest")
```

### Configuring Gemini with different strategies:

```python
# OpenAI-compatible API
gemini_openai = GeminiProvider(
    strategy=OpenAIAPIStrategy(),
    model_name="gemini-2.5-flash"
)

# Native Google SDK
gemini_native = GeminiProvider(
    strategy=GeminiNativeStrategy(),
    model_name="gemini-2.5-pro"
)
```

### Error handling in UI:

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

if not provider.api_key:
    console.print(
        Panel(
            f"API key not found for {provider.name}",
            title="Error",
            border_style="red"
        )
    )
    return
```

## Testing Patterns

### Unit tests:

```python
from unittest.mock import Mock

def test_provider_initialization():
    provider = OllamaProvider(model_name="test-model")
    assert provider.model == "test-model"
    assert provider.name == "Ollama"
```

### Integration tests:

```python
@pytest.mark.integration
def test_ollama_summarization():
    provider = OllamaProvider()
    result = provider.summarize(...)
    assert result is not None
    assert len(result) > 0
```

## Documentation Updates

When suggesting new features, also suggest updates to:

- `README.md` - Add to features list
- `ARCHITECTURE.md` - Explain design decisions
- `QUICKSTART.md` - Add tutorial steps
- `DEPENDENCIES.md` - Document new packages

## Related Files

Key files to reference:
- `AGENTS.md` - Detailed AI agent instructions
- `summarize_webpage/providers/base_provider.py` - Provider pattern
- `summarize_webpage/providers/strategies/base_strategy.py` - Strategy pattern
- `.editorconfig` - Code formatting rules

## Repository Philosophy

> "We're not just writing code that works—we're writing code that teaches."

Every suggestion should:
1. Be understandable to beginners
2. Follow professional patterns
3. Be well-documented
4. Be easily extensible

When in doubt, prioritize **clarity over cleverness**.
