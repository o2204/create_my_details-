from clients.llm_clients.cohere_client import CohereClient
from clients.llm_clients.openai_client import OpenAIClient
from core.constant_manager import CohereModel
from repo.message_repo import MessageRepo
from schemas.message_schema import MessageCreateSchema
import logging
from uuid import UUID
from typing import Optional
from fastapi import UploadFile


class ChatService:
    def __init__(self, cohere_client: CohereClient,
                 openai_client: OpenAIClient,
                 message_repo: MessageRepo,
                 default_model: str = CohereModel.COHEREMODEL):
        
        self.message_repo = message_repo
        self.cohere_client = cohere_client
        self.openai_client = openai_client
        self.default_model = default_model

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"ChatService initialized with default_model: {default_model}")

    async def ask(
    self, conversation_id: str, query: str, 
    model: str | None = None, file: Optional[UploadFile] = None) -> str:
        self.logger.info(
            "ask() called",
            extra={
                "conversation_id": conversation_id,
                "has_file": bool(file),
                "model": model
            }
        )

        try:
            conv_id = UUID(conversation_id)
        except ValueError:
            self.logger.error(
                "Invalid conversation_id format",
                extra={"conversation_id": conversation_id}
            )
            raise ValueError("conversation_id must be a valid UUID")

        if not query or not query.strip():
            self.logger.warning(
                "Empty query received",
                extra={"conversation_id": conv_id}
            )
            raise ValueError("query cannot be empty")

        try:
            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conv_id,
                    role="user",
                    content=query,
                    tokens_used=None
                )
            )
            self.logger.debug(
                "User message saved",
                extra={"conversation_id": conv_id}
            )
        except Exception as e:
            self.logger.error(
                "Failed to save user message",
                exc_info=True,
                extra={"conversation_id": conv_id}
            )
            raise RuntimeError("Failed to save user message") from e

        try:
            if file:
                self.logger.info(
                    "Calling OpenAI with file",
                    extra={"conversation_id": conv_id}
                )
                response = self.openai_client.ask_with_file(
                    query=query,
                    file=file,
                    model="gpt-4o-mini"
                )
            else:
                model_to_use = model or self.default_model
                self.logger.info(
                    "Calling Cohere",
                    extra={
                        "conversation_id": conv_id,
                        "model": model_to_use
                    }
                )
                response = self.cohere_client.ask(
                    prompt=query,
                    model=model_to_use
                )
        except Exception as e:
            self.logger.error(
                "LLM provider call failed",
                exc_info=True,
                extra={"conversation_id": conv_id}
            )
            raise RuntimeError(f"LLM provider failed: {e}") 

        try:
            tokens_used = self.get_tokens_used(query, response)

            await self.message_repo.create(
                MessageCreateSchema(
                    conversation_id=conv_id,
                    role="assistant",
                    content=response,
                    tokens_used=tokens_used
                )
            )
            self.logger.debug(
                "Assistant message saved",
                extra={
                    "conversation_id": conv_id,
                    "tokens_used": tokens_used
                }
            )
        except Exception:
            self.logger.warning(
                "Failed to save assistant message",
                exc_info=True,
                extra={"conversation_id": conv_id}
            )

        self.logger.info(
            "ask() completed successfully",
            extra={"conversation_id": conv_id}
        )
        return response