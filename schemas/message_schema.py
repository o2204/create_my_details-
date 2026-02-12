from pydantic import BaseModel

class MessageCreateSchema(BaseModel):
    conversation_id: str
    role: str  # "user" or "assistant"
    content: str
    tokens_used: int | None = None
    

