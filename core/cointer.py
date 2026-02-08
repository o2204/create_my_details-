import logging
import os
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from repo.create_my_details_repo import CreateMyDetailsRepo
from service.create_my_details_service import CreateMyDetailsService
from clients.llm_clients.cohere_client import CohereClient
from service.chat_service import ChatService

logger = logging.getLogger(__name__)


def get_create_my_details_repo(db: AsyncSession = Depends(get_db)) -> CreateMyDetailsRepo:
    try:
        return CreateMyDetailsRepo(db)
    except Exception as e:
        logger.error(f"Error creating repo: {e}")
        


def get_create_my_details_service(
    repo: CreateMyDetailsRepo = Depends(get_create_my_details_repo),
) -> CreateMyDetailsService:
    try:
        return CreateMyDetailsService(repo)
    except Exception as e:
        logger.error(f"Error creating service: {e}")
        


@lru_cache
def get_cohere_client() -> CohereClient:
    try:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise RuntimeError("COHERE_API_KEY is not set")
        
        return CohereClient(
            api_key=api_key,
            model="command-r7b-12-2024"
        )
    except Exception as e:
        logger.error(f"Error creating Cohere client: {e}")
        


def get_chat_service() -> ChatService:
    try:
        return ChatService(cohere_client=get_cohere_client())
    except Exception as e:
        logger.error(f"Error creating chat service: {e}")
        