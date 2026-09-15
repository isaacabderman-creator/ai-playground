import os
import sys

import httpx
from httpx import Response, HTTPError, HTTPStatusError
from ai_playground.response_model import (
    ModelResponse,
    SystemInstruction,
    Part,
    ModelQuery,
    Content,
)

import dotenv

dotenv.load_dotenv()

MODEL_API_URL = os.getenv("MODEL_API_URL")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")


class GeminiClient:
    def __init__(self, model: str = "gemini-3.5-flash-lite"):
        if not (MODEL_API_URL and MODEL_API_KEY):
            raise NameError("Model API url/key not provided")
        self.model = model
        self.client = httpx.Client(
            base_url=MODEL_API_URL,
            headers={
                "x-goog-api-key": MODEL_API_KEY,
                "Content-Type": "application/json",
            },
        )

    def generate(
        self, contents: list[Content], system_prompt: str | None = None
    ) -> ModelResponse:
        system_instruction = (
            SystemInstruction(parts=[Part(text=system_prompt)])
            if system_prompt
            else None
        )
        model_query = ModelQuery(
            contents=contents, systemInstruction=system_instruction
        )
        try:
            response = (
                self.client.post(
                    f"models/{self.model}:generateContent",
                    json=model_query.model_dump(exclude_none=True),
                )
                .raise_for_status()
                .json()
            )

            return ModelResponse.model_validate(response)
        except HTTPError as e:
            raise RuntimeError(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
