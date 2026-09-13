from enum import Enum
from typing import Literal

from pydantic import BaseModel

class Part(BaseModel):
    text: str
class Content(BaseModel):
    parts: list[Part]
    role: Literal["user", "model"]
class Candidate(BaseModel):
    content: Content
    finishReason: str
    index: int
class ModelResponse(BaseModel):
    candidates: list[Candidate]
    modelVersion: str
    responseId: str