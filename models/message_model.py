import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base

class MessageModel(Base):
    __tablename__ = "messages"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    conversation_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(String, nullable=False)