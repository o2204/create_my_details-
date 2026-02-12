from fastapi import APIRouter, Depends, HTTPException
from service.chat_service import ChatService
from schemas.llm_schema import AskLLMRequest
from core.cointer import get_chat_service

router = APIRouter(prefix="", tags=["Ask LLM Model"])

@router.post("/chat/ask")
async def call_llm_model(
    request: AskLLMRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        # Add await here
        answer = await chat_service.ask(
            conversation_id=request.conversation_id, 
            query=request.query,
            model=request.model
        )
        
        return {
            "conversation_id": request.conversation_id,
            "query": request.query,
            "model": request.model if request.model else chat_service.default_model,
            "answer": answer,
            "tokens_used": chat_service.get_tokens_used(request.query, answer),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )