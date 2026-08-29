from fastapi import APIRouter, Depends, HTTPException
from service.chat_service import ChatService
from schemas.chat_schema import AskLLMRequest
from core.cointer import get_chat_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Ask LLM Model"])

@router.post("/call-llm-model")
async def call_llm_model(
    request: AskLLMRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    logger.info(f"Received request: conversation_id={request.conversation_id}, query='{request.query[:50]}...', model={request.model}")
    logger.info(f"ChatService type: {type(chat_service)}")
    logger.info(f"ChatService methods: {dir(chat_service)}")
    
    try:
        # Try different ways to call the method to see what works
        logger.info("Attempting to call chat_service.ask...")
        
        # Method 1: Direct call
        answer = await chat_service.ask(
            conversation_id=request.conversation_id,
            query=request.query,
            model=request.model
        )
        
        logger.info("Chat service call successful")
        
        return {
            "conversation_id": request.conversation_id,
            "query": request.query,
            "model": request.model if request.model else chat_service.default_model,
            "answer": answer,
            "tokens_used": chat_service.get_tokens_used(request.query, answer),
        }
    except TypeError as e:
        logger.error(f"TypeError in chat_service.ask: {e}", exc_info=True)
        
        # Try to inspect the function signature
        import inspect
        try:
            sig = inspect.signature(chat_service.ask)
            logger.error(f"Expected signature: {sig}")
            logger.error(f"Parameters: {list(sig.parameters.keys())}")
        except:
            pass
            
        raise HTTPException(
            status_code=500,
            detail=f"Method signature error: {str(e)}"
        )
    except ValueError as e:
        logger.error(f"ValueError in chat_service.ask: {e}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat_service.ask: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )