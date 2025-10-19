import os
from .base_provider import BaseProvider
from .strategies.openai_api_strategy import OpenAIAPIStrategy

class OpenAIProvider(BaseProvider):
    """Provider for OpenAI, using the OpenAI API strategy."""

    def __init__(self, model_name=None):
        super().__init__(
            name="OpenAI",
            model=model_name or "gpt-4o-mini",
            strategy=OpenAIAPIStrategy(),
            api_key=os.getenv("OPENAI_API_KEY")
        )
