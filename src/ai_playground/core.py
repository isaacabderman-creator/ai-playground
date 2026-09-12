import json
import os

import httpx
from httpx import Response, URL, HTTPError, HTTPStatusError
from pathlib import Path

import dotenv

dotenv.load_dotenv()

MODEL_API_URL = os.getenv("MODEL_API_URL")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
OUTPUT_PATH = Path(__file__).parent / "sample_reply.json"


def reply(prompt: str) -> dict:
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    if not MODEL_API_URL and MODEL_API_KEY:
        raise NameError("Model API url/key not provided")

    try:
        response: Response = httpx.post(
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
    answer = reply(input("User: "))

    OUTPUT_PATH.write_text(json.dumps(answer, indent=2))
