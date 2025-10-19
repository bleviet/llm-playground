# Dependency Management

This project uses `uv` for fast, reliable Python dependency management.

## Files

- **`pyproject.toml`** - Modern Python project configuration with pinned versions
- **`uv.lock`** - Complete dependency lock file (commit this!)
- **`requirements.txt`** - Human-readable dependency list with pinned versions
- **`requirements-frozen.txt`** - Complete frozen dependencies (all transitive deps)

## Quick Start

### Install dependencies with uv (recommended)

```bash
# Install all dependencies
uv sync

# Install with dev dependencies (pytest, black, ruff, mypy, ipython)
uv sync --all-extras

# After installation, install Playwright browsers
uv run playwright install
```

### Install with pip (alternative)

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install everything including transitive dependencies
pip install -r requirements-frozen.txt

# After installation
python -m playwright install
```

## Current Dependencies (Frozen)

**Python Version:** 3.11+ (currently using 3.13.5)

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| openai | 2.5.0 | OpenAI API SDK (also works with Ollama) |
| google-generativeai | 0.8.5 | Google Gemini native SDK |
| playwright | 1.55.0 | Browser automation for web scraping |
| beautifulsoup4 | 4.14.2 | HTML parsing and text extraction |
| lxml | 6.0.2 | Fast XML/HTML parser |
| python-dotenv | 1.1.1 | Load API keys from .env files |
| rich | 14.2.0 | Beautiful terminal output |

### Development Dependencies (Optional)

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0.0 | Testing framework |
| pytest-asyncio | >=0.21.0 | Async test support |
| black | >=23.0.0 | Code formatter |
| ruff | >=0.1.0 | Fast Python linter |
| mypy | >=1.0.0 | Type checker |
| ipython | 9.6.0 | Enhanced Python REPL |

## Adding Dependencies

```bash
# Add a production dependency
uv add requests

# Add a dev dependency
uv add --dev pytest-cov

# This automatically updates pyproject.toml and uv.lock
```

## Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
uv lock --upgrade

# Update a specific package
uv lock --upgrade-package openai

# Sync the environment after updating
uv sync
```

## Regenerating Frozen Requirements

```bash
# If you need to regenerate requirements-frozen.txt
uv pip freeze > requirements-frozen.txt
```

## Why Both Files?

- **`requirements.txt`**: Human-readable, shows main dependencies only
- **`requirements-frozen.txt`**: Complete freeze including all transitive dependencies
- **`uv.lock`**: Machine-readable lock file used by uv (cross-platform, includes hashes)

## Migration from pip to uv

The project now uses `uv` for faster dependency resolution and installation:
- Up to 10-100x faster than pip
- Built-in virtual environment management
- Reproducible installs via lock file
- Compatible with existing pip workflows

You can still use `pip install -r requirements.txt` if needed!
