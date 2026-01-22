from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repo.create_my_details_repo import CreateMyDetailsRepo
from service.create_my_details_service import CreateMyDetailsService



def get_create_my_details_repo(
        db: AsyncSession = Depends(get_db),
) -> CreateMyDetailsRepo:
    return CreateMyDetailsRepo(db)

def get_create_my_details_service(
        repo: CreateMyDetailsRepo = Depends(get_create_my_details_repo),
) -> CreateMyDetailsService:
    return CreateMyDetailsService(repo)
