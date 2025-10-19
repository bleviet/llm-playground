# LLM Core - Reusable Provider Infrastructure

This is the **shared infrastructure** for working with multiple LLM providers across all projects in this workspace.

## What's Inside

- **Provider Pattern**: Abstract interface for LLM providers
- **Strategy Pattern**: Pluggable API communication strategies
- **Supported Providers**:
  - Ollama (local models)
  - OpenAI (GPT-4, etc.)
  - Google Gemini (dual strategies)
  - Extensible for more!

## Installation

```bash
cd llm_core
pip install -e .
```

Or with uv:
```bash
cd llm_core
uv pip install -e .
```

## Usage

```python
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.ollama import OllamaProvider

# Create a provider
provider = OpenAIProvider(model_name="gpt-4o-mini")

# Get a client
client = provider.get_client()

# Generate a completion
response = provider.summarize(
    client=client,
    website_content="Your content here",
    system_prompt="You are a helpful assistant.",
    user_prompt_prefix="Summarize this: "
)
```

## Environment Variables

Create a `.env` file in your application root (not here):

```env
OPENAI_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
```

## Architecture

See individual applications (like `applications/summarize_webpage/`) for detailed architectural documentation.

This module is designed to be:
- ✅ Framework-agnostic
- ✅ Application-agnostic
- ✅ Easily testable
- ✅ Production-ready

## Provider Examples

### Using Different Providers

```python
from llm_core.providers.openai import OpenAIProvider
from llm_core.providers.ollama import OllamaProvider
from llm_core.providers.gemini import GeminiProvider
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy

# OpenAI
openai = OpenAIProvider(model_name="gpt-4o-mini")

# Ollama (local)
ollama = OllamaProvider(model_name="llama3.2:latest")

# Gemini (OpenAI-compatible API)
gemini = GeminiProvider(
    strategy=OpenAIAPIStrategy(),
    model_name="gemini-2.0-flash-exp"
)

# All have the same interface!
for provider in [openai, ollama, gemini]:
    client = provider.get_client()
    result = provider.summarize(client, content, system_prompt, user_prompt)
```

## Extending with New Providers

1. Inherit from `BaseProvider`
2. Choose or create a strategy
3. Implement any provider-specific logic

```python
from llm_core.providers.base_provider import BaseProvider
from llm_core.providers.strategies.openai_api_strategy import OpenAIAPIStrategy
import os

class AnthropicProvider(BaseProvider):
    def __init__(self, model_name=None):
        super().__init__(
            name="Anthropic",
            model=model_name or "claude-3-5-sonnet-20241022",
            strategy=OpenAIAPIStrategy(),
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
```

## Testing

```python
from unittest.mock import Mock
from llm_core.providers.openai import OpenAIProvider

def test_provider():
    provider = OpenAIProvider(model_name="gpt-4o-mini")
    assert provider.name == "OpenAI"
    assert provider.model == "gpt-4o-mini"
```

## License

MIT License - Free for learning and commercial use
