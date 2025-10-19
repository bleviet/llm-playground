# AI Agent Instructions

This document provides guidance for AI assistants (like GitHub Copilot, Claude, ChatGPT) working on this repository.

## Repository Vision

This is a **learning-focused repository** demonstrating professional software architecture patterns for LLM applications. Every project should be:

1. **Educational** - Code should teach, not just work
2. **Well-Documented** - Extensive comments and architectural explanations
3. **Pattern-Driven** - Use recognized design patterns (Strategy, Factory, etc.)
4. **Production-Ready** - Follow industry best practices
5. **Beginner-Friendly** - Include tutorials and quickstart guides

## Core Principles

### 1. Architecture First

Before suggesting code changes, consider:
- Does this follow SOLID principles?
- Is this the right design pattern for the problem?
- Will beginners understand the architectural decision?
- Have we explained WHY, not just WHAT?

### 2. Documentation Standards

Every project MUST include:
- `README.md` - Overview, architecture diagram, getting started
- `ARCHITECTURE.md` - Deep dive into design patterns and decisions
- `QUICKSTART.md` - 30-minute tutorial for beginners
- `DEPENDENCIES.md` - Dependency management and rationale

### 3. Code Quality

Follow these rules:
- **Type hints** - Use Python type hints where helpful for learning
- **Docstrings** - Every class and non-trivial function needs one
- **Comments** - Explain WHY, not WHAT (code shows what)
- **Naming** - Use clear, self-documenting names
- **Error handling** - Graceful degradation, clear error messages

### 4. Design Pattern Usage

When suggesting patterns:
- **Explain the pattern** - Link to resources, provide diagrams
- **Show alternatives** - Why this pattern over others?
- **Provide examples** - Show both good and bad implementations
- **Consider complexity** - Don't over-engineer for learning projects

## Project Structure Standards

### Required Files

Every project in this repo should have:

```
project_name/
├── README.md              # Main documentation
├── ARCHITECTURE.md        # Design patterns explained
├── QUICKSTART.md          # Beginner tutorial
├── DEPENDENCIES.md        # Dependency rationale
├── pyproject.toml         # Modern Python project config
├── requirements.txt       # Pip-compatible dependencies
├── .env.example          # Example environment variables
└── src/                  # Source code
    ├── core/             # Business logic
    ├── providers/        # External integrations
    └── utils/            # Helpers
```

### Suggested Files

Consider adding:
- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history
- `EXAMPLES.md` - Usage examples
- `TESTING.md` - Testing strategies
- `DEPLOYMENT.md` - Production deployment guide

## Code Review Checklist

When reviewing or generating code, verify:

### Architecture
- [ ] Follows established design patterns
- [ ] SOLID principles respected
- [ ] Clear separation of concerns
- [ ] Proper abstraction levels
- [ ] Dependency injection where appropriate

### Code Quality
- [ ] Type hints present (Python 3.8+)
- [ ] Docstrings for public APIs
- [ ] Comments explain WHY, not WHAT
- [ ] No magic numbers or strings
- [ ] Error handling is comprehensive
- [ ] No code duplication (DRY)

### Documentation
- [ ] README explains what and why
- [ ] ARCHITECTURE.md explains how
- [ ] QUICKSTART.md gets users running in 30 min
- [ ] Code comments are clear and helpful
- [ ] API keys and secrets documented

### Testing
- [ ] Unit tests for core logic
- [ ] Integration tests for API interactions
- [ ] Example usage in docs
- [ ] Edge cases considered

### Security
- [ ] No hardcoded secrets
- [ ] `.env` in `.gitignore`
- [ ] API keys loaded from environment
- [ ] Input validation present
- [ ] Error messages don't leak sensitive info

## Common Patterns in This Repo

### 1. Strategy Pattern

Use when: Multiple algorithms/implementations need to be interchangeable

```python
# Base strategy
class BaseStrategy(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

# Concrete strategies
class StrategyA(BaseStrategy):
    def execute(self, *args, **kwargs):
        # Implementation A
        pass

class StrategyB(BaseStrategy):
    def execute(self, *args, **kwargs):
        # Implementation B
        pass

# Context uses strategy
class Context:
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy  # Dependency injection!
```

**Key points:**
- Strategies are injected, not hardcoded
- Easy to add new strategies without modifying context
- Clear separation between algorithm and usage

### 2. Provider Pattern

Use when: Integrating multiple external services with similar purposes

Example from `summarize_webpage/providers/`:
- `BaseProvider` - Abstract interface
- `OllamaProvider` - Local LLM
- `OpenAIProvider` - Cloud API
- `GeminiProvider` - Google's API

**Key points:**
- All providers inherit from `BaseProvider`
- Each provider encapsulates its configuration
- Strategies handle API differences

### 3. Dependency Injection

Use when: Components need dependencies that might change

```python
# ❌ BAD: Hardcoded dependency
class Service:
    def __init__(self):
        self.client = OpenAI(api_key="...")  # Tightly coupled!

# ✅ GOOD: Injected dependency
class Service:
    def __init__(self, client):
        self.client = client  # Can inject ANY client
```

**Benefits:**
- Easy to test (inject mocks)
- Easy to switch implementations
- Loose coupling

## Language-Specific Guidelines

### Python

**Version:** Python 3.11+ (latest stable recommended)

**Style:**
- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) formatter (100 char line length)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Type hints for public APIs

**Dependencies:**
- Use `pyproject.toml` for modern projects
- Pin versions in `requirements.txt`
- Document WHY dependencies were chosen in `DEPENDENCIES.md`

**Virtual Environments:**
- Always use `venv` or `uv`
- Document setup in README
- Add `.venv/` to `.gitignore`

### Environment Variables

**Always:**
- Use `.env` files (via `python-dotenv`)
- Provide `.env.example` (without real keys)
- Load in base classes, not main scripts
- Document all env vars in README

**Never:**
- Commit `.env` to git
- Hardcode API keys
- Use default secrets in production

## Error Handling Philosophy

### For Learning Projects

**Graceful Degradation:**
```python
try:
    result = api_call()
    return result
except RateLimitError as e:
    return f"Rate limit hit: {e}"  # Keep going with other providers
except Exception as e:
    return f"Error: {e}"  # Don't crash entire script
```

**Why?** Users can compare providers even if one fails.

### For Production Projects

**Fail Fast with Retries:**
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def api_call():
    try:
        return client.request()
    except RateLimitError:
        raise  # Retry
    except AuthenticationError as e:
        logger.error(f"Auth failed: {e}")
        raise  # Don't retry, fail fast
```

## Documentation Templates

### For New Features

When adding a feature, document:

```markdown
## Feature Name

### Purpose
Why does this feature exist?

### Architecture
What design pattern does it use?

### Usage Example
```python
# Clear, runnable example
```

### Extension Points
How can users extend or customize this?

### Trade-offs
What are the pros/cons of this approach?
```

### For New Providers

When adding a provider, include:

1. **Provider class** in `providers/`
2. **Strategy** (if needed) in `providers/strategies/`
3. **Documentation** in README
4. **Example** in QUICKSTART.md
5. **Environment variable** in `.env.example`

## Testing Guidelines

### Unit Tests

Test business logic in isolation:

```python
from unittest.mock import Mock

def test_provider_initialization():
    provider = OpenAIProvider(model_name="gpt-4")
    assert provider.model == "gpt-4"
    assert provider.name == "OpenAI"

def test_summarization_with_mock():
    mock_strategy = Mock()
    mock_strategy.summarize.return_value = "Test summary"
    
    provider = GeminiProvider(strategy=mock_strategy)
    result = provider.summarize(...)
    assert result == "Test summary"
```

### Integration Tests

Test real API interactions (with rate limiting):

```python
import pytest

@pytest.mark.integration
def test_ollama_provider():
    provider = OllamaProvider()
    result = provider.summarize(...)
    assert len(result) > 0
```

## Common Anti-Patterns to Avoid

### ❌ God Objects

Don't create classes that do everything:

```python
# BAD
class LLMManager:
    def fetch_content(self): ...
    def summarize(self): ...
    def format_output(self): ...
    def save_to_file(self): ...
    # ... 500 more lines
```

### ❌ Tight Coupling

Don't hardcode dependencies:

```python
# BAD
class Summarizer:
    def __init__(self):
        self.openai = OpenAI(api_key="...")  # Locked to OpenAI!
```

### ❌ Magic Strings/Numbers

Don't use unexplained constants:

```python
# BAD
if status == 429:  # What does 429 mean?
    retry()

# GOOD
HTTP_RATE_LIMIT = 429
if status == HTTP_RATE_LIMIT:
    retry()
```

### ❌ Silent Failures

Don't hide errors:

```python
# BAD
try:
    result = api_call()
except Exception:
    pass  # User has no idea what went wrong!

# GOOD
try:
    result = api_call()
except Exception as e:
    logger.error(f"API call failed: {e}")
    return f"Error: {e}"
```

## Performance Considerations

### When to Optimize

**Don't optimize prematurely!** For learning projects:
1. ✅ Readability first
2. ✅ Correctness second
3. ✅ Performance third

**Do optimize when:**
- Latency impacts user experience
- Cost is significant (API calls)
- Resource usage is excessive

### Async/Await

Use for I/O-bound operations:

```python
import asyncio

# Sequential (slow)
for provider in providers:
    result = provider.summarize(url)  # Wait for each

# Parallel (fast)
async def summarize_all(providers, url):
    tasks = [provider.summarize_async(url) for provider in providers]
    return await asyncio.gather(*tasks)
```

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Claude provider support
fix: handle rate limit errors gracefully
docs: add architecture diagram to README
refactor: extract strategy pattern to separate module
test: add unit tests for OpenAI provider
chore: update dependencies to latest versions
```

## Review Questions

Before suggesting code, ask:

1. **Architecture**: Does this follow the repo's design philosophy?
2. **Learning**: Will a beginner understand this?
3. **Documentation**: Have we explained the WHY?
4. **Extensibility**: Can users easily customize this?
5. **Best Practices**: Is this how professionals would do it?

## Resources

### Design Patterns
- [Refactoring Guru](https://refactoring.guru/design-patterns)
- [Python Patterns](https://python-patterns.guide/)

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)
- [Effective Python](https://effectivepython.com/)

### Architecture
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## When in Doubt

**Ask these questions:**

1. "Would this make sense to a junior developer?"
2. "Is this the simplest solution that works?"
3. "Have we explained WHY we did it this way?"
4. "Can users easily extend or modify this?"
5. "Does this follow established patterns in the repo?"

## Conclusion

This repository is a **teaching tool**. Every line of code, every design decision, every architectural choice should serve that purpose.

When contributing:
- ✅ Prioritize clarity over cleverness
- ✅ Explain design decisions
- ✅ Show alternatives and trade-offs
- ✅ Make it easy for others to learn and extend

**Remember:** We're not just writing code that works—we're writing code that teaches.
