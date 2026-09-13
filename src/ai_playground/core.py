import os
import sys

import httpx
from httpx import Response, HTTPError, HTTPStatusError

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
        self.context = {"contents": []}

    def reply(self, prompt: str) -> dict:
        _part = {"role": "user", "parts": [{"text": prompt}]}
        self.context["contents"].append(_part)
        try:
            response: Response = self.client.post(
                f"/models/{self.model}:generateContent", json=self.context
            )
            return response.raise_for_status().json()
        except HTTPStatusError as error:
            raise RuntimeError(f"HTTP Status Error: {error}")
        except HTTPError as error:
            raise RuntimeError(f"HTTP Error: {error}")

    def insert_answer(self, answer: str) -> None:
        part = {"role": "model", "parts": [{"text": answer}]}
        self.context["contents"].append(part)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


def main() -> None:
    with GeminiClient() as client:
        while True:
            try:
                prompt = input("user > ")
                response = client.reply(prompt)
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)
            except RuntimeError as e:
                print(e)
                continue
            try:
                answer = response["candidates"][0]["content"]["parts"][0]["text"]
                client.insert_answer(answer)
                print("model > ", answer)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
