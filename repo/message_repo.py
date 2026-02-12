from sqlalchemy.ext.asyncio import AsyncSession
import logging

from models.message_model import MessageModel
from schemas.message_schema import MessageCreateSchema

logger = logging.getLogger(__name__)

class MessageRepo:
    def __init__(self, db: AsyncSession):
        self.db = db 
    
    async def create(self, data: MessageCreateSchema) -> MessageModel:
        try:
            obj = MessageModel(
                conversation_id=data.conversation_id,
                role=data.role,
                content=data.content,
                tokens_used=data.tokens_used,
            )

            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating message object: {e}")
            raise ValueError(f"Invalid data for creating message: {e}")