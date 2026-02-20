from pydantic import BaseModel
from uuid import UUID

class MessageRequestSchema(BaseModel):
    query: str
    model: str | None = None
    k: int | None = None

class MessageResponseSchema(BaseModel):
    query: str 
    model: str 
    answer: str
    tokens_used: int
    k: int | None = None

class MessageCreateSchema(BaseModel):
    conversation_id: UUID
    role: str
    content: str
    tokens_used: int | None = None
