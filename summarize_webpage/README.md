# LLM Web Summarizer - A Beginner's Guide to Multi-Provider LLM Architecture

## 🎯 What This Project Teaches You

This project is a **practical example** of professional software architecture for working with Large Language Models (LLMs). You'll learn:

- ✅ **Strategy Pattern**: How to support multiple LLM providers interchangeably
- ✅ **Dependency Injection**: Injecting different API strategies into providers
- ✅ **Separation of Concerns**: Clean modular code organization
- ✅ **Web Scraping with JavaScript Support**: Using Playwright for dynamic content
- ✅ **Environment Configuration**: Secure API key management
- ✅ **Rich Terminal Output**: Beautiful CLI interfaces with the Rich library

## 🏗️ Project Architecture

```
llm/
├── providers/                 # LLM Provider implementations
│   ├── strategies/           # Different API interaction strategies
│   │   ├── base_strategy.py         # Abstract strategy interface
│   │   ├── openai_api_strategy.py   # OpenAI-compatible API strategy
│   │   └── gemini_native_strategy.py # Google's native Gemini SDK strategy
│   ├── base_provider.py      # Abstract provider base class
│   ├── ollama.py            # Local Ollama provider
│   ├── openai.py            # OpenAI provider
│   └── gemini.py            # Google Gemini provider (dual strategies)
├── core/                     # Core business logic
│   └── summarizer.py        # Summarization orchestration
├── scraper.py               # Web content fetching (Playwright)
├── summarize_webpage.py     # Main application entry point
└── .env                     # API keys (not in git)
```

## 🎨 Design Patterns Explained

### 1. Strategy Pattern

**Problem**: Different LLM providers have different APIs. How do we switch between them without changing our code?

**Solution**: The Strategy Pattern!

```
┌─────────────────┐
│  BaseProvider   │ ◄─── Abstract class defining provider interface
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    │         │          │
┌───▼───┐ ┌──▼────┐ ┌───▼──────┐
│Ollama │ │OpenAI │ │  Gemini  │ ◄─── Concrete providers
└───────┘ └───────┘ └──────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
    ┌─────────▼──────────┐  ┌──────▼────────────┐
    │ OpenAI API Strategy│  │ Native API Strategy│ ◄─── Strategies
    └────────────────────┘  └───────────────────┘
```

**How it works**:
- Each **Provider** (Ollama, OpenAI, Gemini) represents an LLM service
- Each **Strategy** (OpenAI API, Native Gemini API) represents a way to communicate with that service
- Providers delegate API calls to their strategy
- You can use Gemini with **two different strategies**: OpenAI-compatible API or Google's native SDK

### 2. Dependency Injection

Instead of hardcoding dependencies, we **inject** them:

```python
# ❌ BAD: Hardcoded dependency
class GeminiProvider:
    def __init__(self):
        self.strategy = GeminiNativeStrategy()  # Locked to one implementation

# ✅ GOOD: Injected dependency
class GeminiProvider:
    def __init__(self, strategy):
        self.strategy = strategy  # Can use ANY strategy!

# Now you can easily switch:
gemini_with_openai = GeminiProvider(strategy=OpenAIAPIStrategy())
gemini_with_native = GeminiProvider(strategy=GeminiNativeStrategy())
```

### 3. Separation of Concerns

Each module has **one clear responsibility**:

| Module | Responsibility |
|--------|---------------|
| `providers/` | Define LLM providers and how to interact with them |
| `strategies/` | Implement different API communication methods |
| `core/summarizer.py` | Orchestrate the summarization workflow |
| `scraper.py` | Fetch website content |
| `summarize_webpage.py` | Application entry point, configuration |

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### 2. Installation

```bash
# Clone the repository
cd llm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install openai playwright python-dotenv rich beautifulsoup4 google-generativeai

# Install Playwright browsers
python -m playwright install
```

### 3. Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-your-key-here
GEMINI_API_KEY=your-gemini-key-here
```

**Note**: Ollama runs locally and doesn't need an API key.

### 4. Run the Example

```bash
python summarize_webpage.py
```

This will fetch https://edwarddonner.com and generate summaries using all configured providers.

## 📚 Code Walkthrough

### Adding a New Provider

Let's say you want to add **Anthropic Claude**. Here's how:

#### Step 1: Create the Provider Class

Create `providers/claude.py`:

```python
import os
from .base_provider import BaseProvider
from .strategies.openai_api_strategy import OpenAIAPIStrategy

class ClaudeProvider(BaseProvider):
    """Provider for Anthropic Claude."""

    def __init__(self, model_name=None):
        super().__init__(
            name="Anthropic Claude",
            model=model_name or "claude-3-5-sonnet-20241022",
            strategy=OpenAIAPIStrategy(),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url="https://api.anthropic.com/v1"
        )
```

#### Step 2: Add to Main Script

In `summarize_webpage.py`:

```python
from providers.claude import ClaudeProvider

PROVIDERS = [
    OllamaProvider(),
    OpenAIProvider(),
    ClaudeProvider(),  # ← Add your new provider
    # ... rest of providers
]
```

#### Step 3: Add API Key to .env

```env
ANTHROPIC_API_KEY=your-claude-key-here
```

**That's it!** Your new provider is integrated.

### Creating a Custom Strategy

If a provider has a unique API (not OpenAI-compatible), create a custom strategy:

#### Step 1: Create Strategy Class

Create `providers/strategies/claude_native_strategy.py`:

```python
from anthropic import Anthropic
from .base_strategy import BaseStrategy

class ClaudeNativeStrategy(BaseStrategy):
    """Strategy using Anthropic's native SDK."""

    def get_client(self, provider):
        return Anthropic(api_key=provider.api_key)

    def summarize(self, provider, client, website_content, system_prompt, user_prompt_prefix):
        try:
            response = client.messages.create(
                model=provider.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt_prefix + website_content}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"An error occurred with {provider.name}: {e}"
```

#### Step 2: Use the Strategy

```python
from providers.claude import ClaudeProvider
from providers.strategies.claude_native_strategy import ClaudeNativeStrategy

PROVIDERS = [
    ClaudeProvider(strategy=ClaudeNativeStrategy()),  # Use native SDK
]
```

## 🔍 Key Architectural Decisions

### Why `load_dotenv()` is in `base_provider.py`?

**Question**: Why not load environment variables in the main script?

**Answer**: **Encapsulation**. Each provider module should be self-contained and reusable. By loading `.env` in `base_provider.py`:
- ✅ Providers work in ANY script without setup
- ✅ No duplicate code
- ✅ Single source of truth
- ✅ Follows DRY principle

### Why Playwright Instead of `requests`?

**Modern websites use JavaScript** to load content dynamically. The `requests` library only fetches the initial HTML, missing JavaScript-rendered content.

**Playwright**:
- ✅ Renders JavaScript (like a real browser)
- ✅ Waits for network requests to complete
- ✅ Handles modern SPAs (Single Page Applications)
- ❌ Slower than `requests` (acceptable tradeoff)

### Why Rich Library for Output?

Terminal output should be **readable and beautiful**:

```python
# ❌ Plain print
print(f"--- Summary from {provider.name} ---")
print(summary)

# ✅ Rich formatting
console.print(Panel(Markdown(summary), title=f"[cyan]{provider.name}[/cyan]"))
```

Rich provides:
- ✅ Colored panels and borders
- ✅ Markdown rendering in terminal
- ✅ Status spinners during API calls
- ✅ Better user experience

## 🎓 Learning Path

### Beginner Level
1. ✅ Run the project and observe the output
2. ✅ Modify `PROVIDERS` list to use different models
3. ✅ Change the `target_url` to summarize different websites
4. ✅ Modify prompts in `core/summarizer.py`

### Intermediate Level
1. ✅ Add a new provider (e.g., Anthropic Claude, Cohere)
2. ✅ Create a custom prompt for a specific use case
3. ✅ Add error handling and retry logic
4. ✅ Implement caching for website content

### Advanced Level
1. ✅ Create a new strategy for a non-OpenAI-compatible API
2. ✅ Add support for streaming responses
3. ✅ Implement rate limiting and cost tracking
4. ✅ Build a CLI with argument parsing (e.g., `argparse` or `click`)
5. ✅ Add unit tests and integration tests

## 🛠️ Extending the Project

### Ideas for Enhancement

1. **Add More Providers**
   - Anthropic Claude
   - Cohere
   - Hugging Face Inference API
   - Local models via Transformers

2. **Different Use Cases**
   - Document Q&A
   - Code explanation
   - Translation
   - Sentiment analysis

3. **Advanced Features**
   - Streaming responses
   - Cost tracking per provider
   - Response comparison dashboard
   - Batch processing multiple URLs
   - Export results to JSON/CSV

4. **Production Readiness**
   - Logging with `structlog`
   - Configuration management with `pydantic`
   - Async/await for parallel processing
   - Docker containerization
   - API wrapper with FastAPI

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
ImportError: cannot import name 'sync_playwright'
```
**Solution**: Install Playwright browsers: `python -m playwright install`

**API Key Not Found**
```
API key for OpenAI not found. Skipping.
```
**Solution**: Check your `.env` file and ensure it's in the project root.

**Google Library Warnings**
```
WARNING: All log messages before absl::InitializeLog()...
```
**Solution**: These are suppressed in `providers/strategies/gemini_native_strategy.py`. If still appearing, the suppression logic may need adjustment based on your OS.

## 📖 Further Reading

- [Strategy Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/strategy)
- [Dependency Injection Explained](https://www.freecodecamp.org/news/a-quick-intro-to-dependency-injection-what-it-is-and-when-to-use-it-7578c84fa88f/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini API](https://ai.google.dev/docs)
- [Playwright Python](https://playwright.dev/python/)

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new providers
- Improve documentation
- Fix bugs
- Add examples

## 📄 License

MIT License - Free to use for learning and commercial projects.

---

**Happy Learning!** 🚀

If you have questions or suggestions, please open an issue or discussion.
