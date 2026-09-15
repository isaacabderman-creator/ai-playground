from httpx import HTTPStatusError, Response, HTTPError

from ai_playground.client import GeminiClient
from ai_playground.response_model import ModelResponse


class ChatSession:
    def __init__(self, client: GeminiClient):
        self.context = {"contents": []}
        self.client = client

    def chat(self, text):
        part = {"role": "user", "parts": [{"text": text}]}
        self.context["contents"].append(part)
        response: ModelResponse = self.client.generate(self.context["contents"])
        answer = response.candidates[0].content.parts[0].text
        part = {"role": "model", "parts": [{"text": answer}]}
        self.context["contents"].append(part)
        return answer
