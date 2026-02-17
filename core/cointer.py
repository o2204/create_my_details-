from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from repo.create_my_details_repo import CreateMyDetailsRepo
from repo.message_repo import MessageRepo
from service.create_my_details_service import CreateMyDetailsService
from clients.llm_clients.cohere_client import CohereClient
from clients.llm_clients.openai_client import OpenAIClient
from service.chat_service import ChatService
from core.config import Settings, get_settings
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
    
# Fix 1: Remove the duplicate get_chat_service without db parameter
# Fix 2: Fix get_cohere_client to not use Depends
def get_cohere_client() -> CohereClient:
    try:
        settings = get_settings()  # Call the function directly, not through Depends
        return CohereClient(
            api_key=settings.COHERE_API_KEY,
        )
    except Exception as e:
        raise Exception(f"Error creating Cohere client: {e}")  

def get_openai_client() -> OpenAIClient:
    try: 
        settings = get_settings()
        return OpenAIClient(
            api_key=settings.OPENAI_API_KEY
        )
    except Exception as e:
        raise Exception(f"Error creating OpenAI client: {e}")

# Fix 3: Keep this version with db parameter
def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    try:
        message_repo = MessageRepo(db)

        cohere_client = get_cohere_client()
        openai_client = get_openai_client()

        return ChatService(
            cohere_client=cohere_client,
            openai_client=openai_client,
            message_repo=message_repo,
            default_model=CohereModel.COHEREMODEL
        )
    except Exception as e:
        raise Exception(f"Error creating chat service: {e}")