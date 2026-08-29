from sqlalchemy.ext.asyncio import AsyncSession
import logging

from models.create_my_details_model import CreateMyDetailsModel
from schemas.create_my_details_schemas import CreateRequestSchema

logger = logging.getLogger(__name__)

class CreateMyDetailsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db 
    
    async def create(self, data: CreateRequestSchema) -> CreateMyDetailsModel:
        try:
            obj = CreateMyDetailsModel(
                name=data.name,
                age=data.age,
                address=data.address,
            )
            
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Unexpected error: {e}")
            raise ValueError(f"Error creating details: {e}")