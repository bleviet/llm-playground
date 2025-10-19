# LLM Playground - Professional Architecture for LLM Applications

A **learning-focused workspace** demonstrating professional software architecture patterns for building LLM applications.

## 🎯 Repository Vision

This repository teaches you how to:
- ✅ Build **reusable** LLM provider infrastructure
- ✅ Apply **design patterns** (Strategy, Provider, Dependency Injection)
- ✅ Follow **SOLID principles** in real projects
- ✅ Structure **multi-application** workspaces
- ✅ Write **production-ready** code

## 📁 Repository Structure

```
llm-playground/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot guidance
├── AGENTS.md                       # AI agent instructions
├── .editorconfig                   # Editor settings
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── llm_core/                       # 🔧 Shared LLM provider infrastructure
│   ├── README.md
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── .env.example
│   ├── providers/                  # Provider implementations
│   │   ├── base_provider.py
│   │   ├── ollama.py
│   │   ├── openai.py
│   │   ├── gemini.py
│   │   └── strategies/             # API communication strategies
│   │       ├── base_strategy.py
│   │       ├── openai_api_strategy.py
│   │       └── gemini_native_strategy.py
│   └── utils/                      # Shared utilities
│
└── applications/                   # 📱 Applications using llm_core
    └── summarize_webpage/          # Web summarization app
        ├── README.md
        ├── ARCHITECTURE.md
        ├── QUICKSTART.md
        ├── DEPENDENCIES.md
        ├── pyproject.toml
        ├── requirements.txt
        ├── .env.example
        ├── scraper.py
        ├── summarize_webpage.py
        └── core/
            └── summarizer.py
```

## 🔧 LLM Core (Shared Infrastructure)

**Purpose**: Reusable provider pattern for multiple LLM services

**Features**:
- Abstract provider interface
- Strategy pattern for different APIs
- Support for Ollama, OpenAI, Gemini
- Easy to extend with new providers

**Usage**:
```python
from llm_core.providers.openai import OpenAIProvider

provider = OpenAIProvider(model_name="gpt-4o-mini")
client = provider.get_client()
response = provider.summarize(client, content, system_prompt, user_prompt)
```

See [`llm_core/README.md`](llm_core/README.md) for details.

## 📱 Applications

### 1. Summarize Webpage

**What it does**: Fetches web content and generates summaries using multiple LLM providers

**Key features**:
- JavaScript-enabled web scraping (Playwright)
- Side-by-side provider comparison
- Beautiful terminal output (Rich)

**Quick start**:
```bash
# 1. Install llm_core
cd llm_core
pip install -e .

# 2. Install application
cd ../applications/summarize_webpage
pip install -r requirements.txt
python -m playwright install

# 3. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 4. Run
python summarize_webpage.py
```

See [`applications/summarize_webpage/README.md`](applications/summarize_webpage/README.md) for details.

## 🚀 Getting Started

### 1. Install llm_core (required)

```bash
cd llm_core
pip install -e .
```

Or with uv:
```bash
cd llm_core
uv pip install -e .
```

The `-e` flag installs in "editable" mode, so changes to `llm_core` are immediately available.

### 2. Choose an application

```bash
cd applications/summarize_webpage
pip install -r requirements.txt
python -m playwright install
```

### 3. Configure API keys

Create `.env` in the application directory:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```env
OPENAI_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
```

### 4. Run

```bash
python summarize_webpage.py
```

## 🎓 Learning Path

### Beginner
1. Run `summarize_webpage` and observe output
2. Read [`llm_core/README.md`](llm_core/README.md) to understand providers
3. Modify prompts in `applications/summarize_webpage/core/summarizer.py`
4. Try different models by editing `summarize_webpage.py`

### Intermediate
1. Add a new provider (e.g., Anthropic Claude) to `llm_core`
2. Create a new application using `llm_core`
3. Read [`applications/summarize_webpage/ARCHITECTURE.md`](applications/summarize_webpage/ARCHITECTURE.md)
4. Implement error handling improvements

### Advanced
1. Add streaming support to providers
2. Implement async parallel processing
3. Build a web API wrapper with FastAPI
4. Add comprehensive test suite
5. Create a new strategy for a different API type

## 📚 Documentation

- [`AGENTS.md`](AGENTS.md) - AI agent instructions for this repo
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md) - GitHub Copilot guidance
- [`llm_core/README.md`](llm_core/README.md) - Provider infrastructure docs
- [`applications/summarize_webpage/ARCHITECTURE.md`](applications/summarize_webpage/ARCHITECTURE.md) - Design patterns explained
- [`applications/summarize_webpage/QUICKSTART.md`](applications/summarize_webpage/QUICKSTART.md) - 30-minute tutorial

## 🏗️ Architecture Philosophy

### Separation of Concerns

```
llm_core/          → "How do I talk to LLMs?"
applications/      → "What do I do with LLMs?"
```

**Benefits**:
- Providers can be reused across multiple applications
- Changes to providers don't affect applications
- Easy to test each layer independently
- Clear boundaries and responsibilities

### Design Patterns

- **Strategy Pattern**: Pluggable API communication strategies
  - `OpenAIAPIStrategy` - Works with OpenAI-compatible APIs
  - `GeminiNativeStrategy` - Uses Google's native SDK
  - Easy to add new strategies without modifying providers

- **Provider Pattern**: Unified interface for multiple LLM services
  - `BaseProvider` - Abstract interface
  - `OllamaProvider`, `OpenAIProvider`, `GeminiProvider` - Concrete implementations
  - All providers have the same interface

- **Dependency Injection**: Flexible, testable components
  - Strategies are injected into providers
  - Providers are injected into applications
  - Easy to mock for testing

### SOLID Principles

Every module follows:
- **S**ingle Responsibility - Each class has one reason to change
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - Providers are interchangeable
- **I**nterface Segregation - Focused interfaces
- **D**ependency Inversion - Depend on abstractions, not concretions

## 🛠️ Future Applications

Ideas for new applications using `llm_core`:

1. **Document Q&A** - Ask questions about PDFs/docs
2. **Code Explainer** - Analyze and explain code
3. **Sentiment Analyzer** - Analyze text sentiment
4. **Translation Tool** - Multi-provider translation
5. **Meeting Summarizer** - Summarize transcripts
6. **Email Composer** - Draft emails with different tones
7. **Content Generator** - Generate blog posts, social media
8. **Data Analyst** - Natural language data queries

Each application:
- Uses `llm_core` providers
- Has its own dependencies
- Follows the same architectural patterns
- Lives in `applications/` directory

## 🤝 Contributing

This is a learning project! Contributions welcome:
- Add new providers to `llm_core`
- Build new applications
- Improve documentation
- Add tests
- Fix bugs

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for coding guidelines.

## 📄 License

MIT License - Free for learning and commercial use

---

## 🔍 Why This Structure?

### Before: Monolithic
```
summarize_webpage/
├── providers/         # Locked inside one app
└── app logic
```

**Problems**:
- Can't reuse providers
- Duplicates code for new apps
- Hard to maintain

### After: Modular
```
llm_core/              # Reusable infrastructure
applications/          # Multiple apps sharing llm_core
```

**Benefits**:
- ✅ Reuse providers everywhere
- ✅ Add apps easily
- ✅ Test independently
- ✅ Professional structure

---

**Happy Learning!** 🚀

*Remember: We're not just writing code that works—we're writing code that teaches.*
