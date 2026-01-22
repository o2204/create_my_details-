from sqlalchemy.ext.asyncio import AsyncSession
from models.create_my_details_model import CreateMyDetailsModel
from schemas.create_my_details_schemas import CreateMyRequestSchema 


class CreateMyDetailsRepo:
    def __init__(self, db: AsyncSession):
        self.db = db 
    
    async def create(
            self, 
            data: CreateMyRequestSchema,
    ) -> CreateMyDetailsModel:
        
        obj = CreateMyDetailsModel(
            name=data.name,
            age=data.age,
            add=data.add,
        )

        self.db.add(obj)
        
        await self.db.refresh(obj)

        return obj 