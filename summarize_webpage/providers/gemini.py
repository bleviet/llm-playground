import os
from .base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    """Provider for Google Gemini, with a configurable strategy."""

    def __init__(self, strategy, model_name=None):
        # Determine model and name based on strategy
        if "Native" in strategy.__class__.__name__:
            name = "Google Gemini (Native)"
            model = model_name or "gemini-2.5-pro"
        else:
            name = "Google Gemini (OpenAI API)"
            model = model_name or "gemini-2.5-flash"

        super().__init__(
            name=name,
            model=model,
            strategy=strategy,
            api_key=os.getenv("GEMINI_API_KEY"),
            # Base URL is only relevant for OpenAI-compatible APIs
            base_url="https://generativelanguage.googleapis.com/v1beta" if "Native" not in strategy.__class__.__name__ else None
        )
