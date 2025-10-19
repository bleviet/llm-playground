from abc import ABC
from dotenv import load_dotenv

# Load environment variables from .env file when this module is first imported.
# This is done here (in the base class) so all providers benefit without duplication.
# The override=True ensures we use .env values even if they're already in the environment.
load_dotenv(override=True)

class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.

    This class uses the Strategy Pattern: providers define WHAT service they represent
    (Ollama, OpenAI, Gemini), while strategies define HOW to communicate with them.

    Why abstract? We never create a BaseProvider directly - only concrete providers
    like OllamaProvider or GeminiProvider. The ABC (Abstract Base Class) enforces this.
    """

    def __init__(self, name, model, strategy, api_key=None, base_url=None):
        """
        Initialize a provider with its configuration.

        Args:
            name: Human-readable name (e.g., "OpenAI", "Ollama")
            model: Model identifier (e.g., "gpt-4o-mini", "llama3.2:latest")
            strategy: The strategy object that handles API communication
            api_key: API key for authentication (None for local models)
            base_url: Custom API endpoint (None uses provider's default)
        """
        self.name = name
        self.model = model
        self.strategy = strategy  # This is Dependency Injection!
        self.api_key = api_key
        self.base_url = base_url

    def get_client(self):
        """
        Create and return an API client for this provider.

        This method delegates to the strategy because different APIs need different
        client configurations. For example:
        - OpenAI: OpenAI(api_key=key)
        - Gemini: genai.configure(api_key=key)

        Returns:
            An API client object (type depends on the strategy)
        """
        return self.strategy.get_client(self)

    def summarize(self, client, website_content, system_prompt, user_prompt_prefix):
        """
        Generate a summary of website content using this provider.

        This method delegates to the strategy because different APIs have different
        ways of formatting requests and parsing responses.

        Args:
            client: API client (created by get_client())
            website_content: The text content to summarize
            system_prompt: Instructions about how the LLM should behave
            user_prompt_prefix: Prefix for the user message

        Returns:
            str: The generated summary
        """
        return self.strategy.summarize(self, client, website_content, system_prompt, user_prompt_prefix)
