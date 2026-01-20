from fastapi import APIRouter, status,Depends
from src.LLMChatBot.schemas import UserMessage,LLMKeyData
from src.LLMChatBot.service import ChatService
from sqlalchemy.orm import Session
from src.database import get_async_session
router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def llm_chat(user_message: UserMessage, db: Session = Depends(get_async_session)) -> dict:
    return await ChatService(db).llm_chat(message=user_message.message)


@router.post(
    "/saveLLMKey",
    status_code=status.HTTP_200_OK,
)
async def save_llm_key(api_key: LLMKeyData,db: Session = Depends(get_async_session)) -> dict:
    return await ChatService(db).save_llm_key(message=api_key.key)


