from schemas.create_my_details_schemas import CreateMyRequestSchema, CreateMyResponseSchema
from repo.create_my_details_repo import CreateMyDetailsRepo


class CreateMyDetailsService:
    def __init__(self, repo:CreateMyDetailsRepo):
        self.repo = repo 

    async def create_my_details(
            self,
            data: CreateMyRequestSchema,
    ) -> CreateMyResponseSchema:
        
        obj = await self.repo.create(data)
        await self.repo.commit()

        return CreateMyRequestSchema(
            name=obj.name,
            age=obj.age,
            add=obj.add,
        )