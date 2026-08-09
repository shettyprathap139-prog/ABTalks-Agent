from pydantic import BaseModel
from typing import List


class PostCreate(BaseModel):
    text: str
    rationale: str
    sources: List[str]