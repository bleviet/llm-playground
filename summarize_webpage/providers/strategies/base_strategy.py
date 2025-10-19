from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """Abstract base class for provider strategies."""

    @abstractmethod
    def get_client(self, provider):
        """Returns an API client for the provider."""
        pass

    @abstractmethod
    def summarize(self, provider, client, website_content, system_prompt, user_prompt_prefix):
        """Generates a summary for the given content."""
        pass
