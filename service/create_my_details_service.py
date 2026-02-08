from schemas.create_my_details_schemas import CreateMyRequestSchema, CreateMyResponseSchema
from repo.create_my_details_repo import CreateMyDetailsRepo
from exceptions.create_my_details_exception import (
    NameNotFound,
    AgeNotFound,
    AddressNotFound,
)

class CreateMyDetailsService:
    def __init__(self, repo:CreateMyDetailsRepo):
        self.repo = repo 
    
    async def create_my_details(
            self,
            data: CreateMyRequestSchema,
    ) -> CreateMyResponseSchema:
        
        if not data.name or not data.name.strip():
            raise NameNotFound(data.name, exception_type="This's in service layer") 
        if data.age is None or data.age <= 0:
            raise AgeNotFound(data.age)

        if not data.address or not data.address.strip():
            raise AddressNotFound(data.address)
        
        obj = await self.repo.create(data)

        return CreateMyResponseSchema(
            name=obj.name,
            age=obj.age,
            address=obj.address,
        )