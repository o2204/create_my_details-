from fastapi import APIRouter, Depends, HTTPException
from service.chat_service import ChatService
from schemas.llm_schema import AskLLMRequest
from core.cointer import get_chat_service

router = APIRouter(prefix="", tags=["Ask LLM Model"])


@router.post("/call-llm-model")
async def call_llm_model(
    request: AskLLMRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        answer = chat_service.ask(request.query)
        return {
            "query": request.query,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
