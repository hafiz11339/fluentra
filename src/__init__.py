from src.LLMChatBot.router import router as llmchatbot_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(llmchatbot_router, tags=["ChatBot"], prefix="/chatbot")
