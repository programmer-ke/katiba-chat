"""Generation Adapters"""

from openai import OpenAI

from .. import core


class OpenAICompatibleLLM(core.AbstractLLM):

    OPENAI_BASE_URL = "https://api.openai.com/v1"

    def __init__(
        self, model_name: str, api_key, base_url: str = OPENAI_BASE_URL
    ):
        self.model_name = model_name
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def generate(self, prompt):
        request_args = self.format_completions_request(
            self.model_name, str(prompt)
        )
        response = self.client.chat.completions.create(**request_args)
        generated_text = response.choices[0].message.content
        return core.LLMResponse(generated_text)

    @staticmethod
    def format_completions_request(model_name: str, prompt: str):
        return {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
        }
