from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.create_my_details_model import CreateMyDetailsModel
from schemas.create_my_details_schemas import CreateMyRequestSchema
from exceptions.custome_exception import CustomException


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
            address=data.address,
        )

        try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj

        except IntegrityError as e:
            await self.db.rollback()
            raise CustomException(
                status_code=409,
                detail="Database integrity violation",
                exception_type="IntegrityError",
                additional_info={
                    "original_error": str(e),
                },
            )

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise CustomException(
                status_code=500,
                detail="Database operation failed",
                exception_type="DatabaseError",
                additional_info={
                    "original_error": str(e),
                },
            )
