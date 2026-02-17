from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class AskLLMRequest(BaseModel):
    conversation_id: str
    query: str
    model: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        conversation_id: str = Form(...),
        query: str = Form(...),
        model: Optional[str] = Form(None),
    ):
        return cls(
            conversation_id=conversation_id,
            query=query,
            model=model
        )
