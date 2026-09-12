import os

import httpx
from httpx import Response, URL, HTTPError, HTTPStatusError

import dotenv

dotenv.load_dotenv()

MODEL_API_URL = os.getenv("MODEL_API_URL")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")


class GeminiClient:
    def __init__(self):
        self.client = httpx.Client()

    def reply(self, prompt: str) -> dict:
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
        }
        if not (MODEL_API_URL and MODEL_API_KEY):
            raise NameError("Model API url/key not provided")

        try:
            response: Response = self.client.post(
                MODEL_API_URL,
                headers={
                    "x-goog-api-key": MODEL_API_KEY,
                    "Content-Type": "application/json",
                },
                json=body,
            )
            return response.raise_for_status().json()
        except HTTPStatusError as e:
            raise RuntimeError(f"HTTP Status Error: {e}")
        except HTTPError as e:
            raise RuntimeError(f"HTTP Error: {e}")


if __name__ == "__main__":
    client = GeminiClient()
    print(client.reply("Hello World"))
