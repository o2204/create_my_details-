from pydantic import BaseModel


class AskLLMRequest(BaseModel):
    query: str
