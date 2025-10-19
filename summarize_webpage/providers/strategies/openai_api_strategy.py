from openai import OpenAI
from .base_strategy import BaseStrategy

class OpenAIAPIStrategy(BaseStrategy):
    """Strategy for providers using the OpenAI API/SDK."""

    def get_client(self, provider):
        if provider.base_url:
            return OpenAI(base_url=provider.base_url, api_key=provider.api_key)
        return OpenAI(api_key=provider.api_key)

    def summarize(self, provider, client, website_content, system_prompt, user_prompt_prefix):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_prefix + website_content},
        ]
        try:
            response = client.chat.completions.create(
                model=provider.model, messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred with {provider.name}: {e}"
