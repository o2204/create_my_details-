from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from repo.create_my_details_repo import CreateMyDetailsRepo
from service.create_my_details_service import CreateMyDetailsService
from clients.llm_clients.cohere_client import CohereClient
from service.chat_service import ChatService
from core.config import get_settings 
from core.constant_manager import CohereModel


def get_create_my_details_repo(db: AsyncSession = Depends(get_db)) -> CreateMyDetailsRepo:
    try:
        return CreateMyDetailsRepo(db)
    except Exception as e:
        raise Exception(f"Error creating repo: {e}")
        
def get_create_my_details_service(
    repo: CreateMyDetailsRepo = Depends(get_create_my_details_repo),
) -> CreateMyDetailsService:
    try:
        return CreateMyDetailsService(repo)
    except Exception as e:
        raise Exception(f"Error creating service: {e}")
    
def get_chat_service() -> ChatService:
    try:
        return ChatService(cohere_client=get_cohere_client())
    except Exception as e:
        raise Exception(f"Error creating chat service: {e}")

def get_cohere_client(settings: get_settings = Depends(get_settings)) -> CohereClient:
    try:
        return CohereClient(
            api_key=settings.COHERE_API_KEY,
            model= CohereModel.COHEREMODEL,
        )
    except Exception as e:
        raise Exception(f"Error creating Cohere client: {e}")  
        