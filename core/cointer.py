from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from repo.create_my_details_repo import CreateMyDetailsRepo
from service.create_my_details_service import CreateMyDetailsService

from clients.llm_clients.cohere_client import CohereClient
from routers.llm_router import LLMRouter
from service.chat_service import ChatService

import os
from functools import lru_cache


def get_create_my_details_repo(
        db: AsyncSession = Depends(get_db),
) -> CreateMyDetailsRepo:
    return CreateMyDetailsRepo(db)

def get_create_my_details_service(
        repo: CreateMyDetailsRepo = Depends(get_create_my_details_repo),
) -> CreateMyDetailsService:
    return CreateMyDetailsService(repo)




@lru_cache
def get_cohere_client() -> CohereClient:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("COHERE_API_KEY is not set")

    return CohereClient(
        api_key=api_key,
        model="command-r7b-12-2024"
    )

def get_chat_service() -> ChatService:
    return ChatService(
        cohere_client=get_cohere_client()   
    )