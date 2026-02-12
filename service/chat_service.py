from clients.llm_clients.cohere_client import CohereClient
from core.constant_manager import CohereModel
from repo.message_repo import MessageRepo
from schemas.message_schema import MessageCreateSchema
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, cohere_client: CohereClient,
                 message_repo: MessageRepo,
                 default_model: str = CohereModel.COHEREMODEL):
        
        self.message_repo = message_repo
        self.cohere_client = cohere_client
        self.default_model = default_model

    async def ask(self, conversation_id: str, query: str, model: str | None = None) -> str:
        try: 
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            model_to_use = model if model else self.default_model
            
            # Save user message
            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conversation_id,
                    role="user",
                    content=query,
                    metadata={},
                )
            )

            # Get response from Cohere
            response = self.cohere_client.ask(
                prompt=query,
                model=model_to_use,
            )

            tokens_used = self.get_tokens_used(query, response)
            
            # Save assistant message - now await
            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=response,
                    tokens_used=tokens_used,
                    metadata={},
                )
            )
            return response
        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            raise ValueError(f"Error processing chat request: {e}")
        
    def get_tokens_used(self, query: str, answer: str) -> int:
        return len(query.split()) + len(answer.split())