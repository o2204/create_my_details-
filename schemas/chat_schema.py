from pydantic import BaseModel


class AskLLMRequest(BaseModel):
    conversation_id: str 
    query: str
    model: str | None = None
    k: int | None = None
