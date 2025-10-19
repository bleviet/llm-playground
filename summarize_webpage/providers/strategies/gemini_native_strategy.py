import os
import logging

# Suppress noisy warnings from Google libraries.
# This should be done before other imports.
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'  # 0=INFO, 1=WARN, 2=ERROR, 3=FATAL
logging.getLogger('google.generativeai').setLevel(logging.ERROR)
logging.getLogger('google.api_core').setLevel(logging.ERROR)

import google.generativeai as genai
from .base_strategy import BaseStrategy

class GeminiNativeStrategy(BaseStrategy):
    """Strategy for Gemini using the native Google Generative AI SDK."""

    def get_client(self, provider):
        genai.configure(api_key=provider.api_key)
        return genai.GenerativeModel(provider.model)

    def summarize(self, provider, client, website_content, system_prompt, user_prompt_prefix):
        # Gemini has a different way of handling system prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt_prefix}\n\n{website_content}"
        try:
            response = client.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"An error occurred with {provider.name} (Native): {e}"
