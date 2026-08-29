from sqlalchemy.ext.asyncio import AsyncSession
import logging
from uuid import UUID

from models.message_model import MessageModel
from schemas.message_schema import MessageCreateSchema

logger = logging.getLogger(__name__)

class MessageRepo:
    def __init__(self, db: AsyncSession):
        self.db = db 
    
    async def create(self, data: MessageCreateSchema) -> MessageModel:
        try:
            # Ensure conversation_id is a UUID object, not a string
            conv_id = data.conversation_id
            if isinstance(conv_id, str):
                conv_id = UUID(conv_id)
            
            obj = MessageModel(
                conversation_id=conv_id,  # Pass UUID object directly
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