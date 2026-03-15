

import os

from .base_model import ModelWrapper
import google.genai as genai

class GeminiWrapper(ModelWrapper):
    def __init__(self, model_name, api_key=None):
        super().__init__()
        self.model_name = model_name
        if api_key is None:
            self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def get_client(self):
        return self.client

    def generate(self, prompt):
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text
