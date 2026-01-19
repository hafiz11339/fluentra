from fastapi import APIRouter, Depends, status, Request, File, UploadFile, Query
from src.LLMChatBot.schemas import UserMessage
from src.LLMChatBot.service import ChatService
router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def llm_chat(user_message: UserMessage) -> dict:
    return await ChatService().llm_chat(message=user_message.message)


