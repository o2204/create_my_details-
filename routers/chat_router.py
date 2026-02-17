from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional
from service.chat_service import ChatService
from schemas.chat_schema import AskLLMRequest
from core.cointer import get_chat_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Ask LLM Model"])


@router.post("/call-llm-model")
async def call_llm_model(
    request: AskLLMRequest = Depends(AskLLMRequest.as_form),
    file: Optional[UploadFile] = None,
    chat_service: ChatService = Depends(get_chat_service)
):

    logger.info(
        "Received call-llm-model request",
        extra={
            "conversation_id": request.conversation_id,
            "has_file": bool(file),
            "model": request.model,
            "filename": file.filename if file else None,
        }
    )

    if not request.query or not request.query.strip():
        logger.warning(
            "Empty query received",
            extra={"conversation_id": request.conversation_id}
        )
        raise HTTPException(
            status_code=400,
            detail="query cannot be empty"
        )

    try:
        answer = await chat_service.ask(
            conversation_id=request.conversation_id,
            query=request.query,
            model=request.model,
            file=file
        )
    except ValueError as e:
        logger.warning(
            "Validation error in chat_service.ask",
            exc_info=True,
            extra={"conversation_id": request.conversation_id}
        )
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(
            "Runtime error in chat_service.ask",
            exc_info=True,
            extra={"conversation_id": request.conversation_id}
        )
        raise HTTPException(
            status_code=502,
            detail="LLM provider failed"
        )
    except Exception as e:
        logger.error(
            "Unexpected error in call_llm_model",
            exc_info=True,
            extra={"conversation_id": request.conversation_id}
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    logger.info(
        "call-llm-model completed successfully",
        extra={"conversation_id": request.conversation_id}
    )

    return {
        "conversation_id": request.conversation_id,
        "model": request.model or chat_service.default_model,
        "answer": answer,
    }
