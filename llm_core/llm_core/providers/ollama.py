from .base_provider import BaseProvider
from .strategies.openai_api_strategy import OpenAIAPIStrategy

class OllamaProvider(BaseProvider):
    """Provider for Ollama, using the OpenAI API strategy."""

    def __init__(self, model_name=None):
        super().__init__(
            name="Ollama",
            model=model_name or "llama3.2:latest",
            strategy=OpenAIAPIStrategy(),
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )
