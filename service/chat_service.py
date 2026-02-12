from clients.llm_clients.cohere_client import CohereClient
from core.constant_manager import CohereModel
from repo.message_repo import MessageRepo
from schemas.message_schema import MessageCreateSchema
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, cohere_client: CohereClient,
                 message_repo: MessageRepo,
                 default_model: str = CohereModel.COHEREMODEL):
        
        self.message_repo = message_repo
        self.cohere_client = cohere_client
        self.default_model = default_model
        logger.info(f"ChatService initialized with default_model: {default_model}")

    async def ask(self, conversation_id: str, query: str, model: str | None = None) -> str:
        logger.info(f"ask() called with conversation_id: {conversation_id}, query: '{query[:50]}...', model: {model}")
        
        try: 
            if not query or not query.strip():
                raise ValueError("Query cannot be empty")
            
            model_to_use = model if model else self.default_model
            logger.info(f"Using model: {model_to_use}")
            
            # Convert conversation_id to UUID if it's a string
            try:
                conv_id = UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id
                logger.info(f"Converted conversation_id to UUID: {conv_id}")
            except ValueError:
                raise ValueError(f"Invalid conversation_id format: {conversation_id}")
            
            # Save user message
            logger.info("Saving user message to database...")
            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conv_id,
                    role="user",
                    content=query,
                    tokens_used=None,
                )
            )

            # Get response from Cohere
            logger.info("Calling Cohere API...")
            response = self.cohere_client.ask(
                prompt=query,
                model=model_to_use,
            )
            logger.info(f"Cohere response received: {response[:50]}...")

            tokens_used = self.get_tokens_used(query, response)
            logger.info(f"Tokens used: {tokens_used}")
            
            # Save assistant message
            logger.info("Saving assistant message to database...")
            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conv_id,
                    role="assistant",
                    content=response,
                    tokens_used=tokens_used,
                )
            )
            
            logger.info("Chat request completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing chat request: {e}", exc_info=True)
            raise ValueError(f"Error processing chat request: {e}")
        
    def get_tokens_used(self, query: str, answer: str) -> int:
        return len(query.split()) + len(answer.split())