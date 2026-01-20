from dotenv import load_dotenv
import os
from src.settings import settings
from src.response import BuildJSONResponses
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.LLMChatBot.prompt import SYSTEM_PROMPT
from src.LLMChatBot.models import LLMKeys
from src.LLMChatBot.utils import encrypt_text, decrypt_text
from sqlalchemy import select
from typing import Optional

class ChatService:
    def __init__(self, db):
        self.db = db
        self.model = LLMKeys
        self.chat: Optional[ChatOpenAI] = None

    async def _fetch_plain_key(self):
        result = await self.db.execute(select(self.model))
        row = result.scalars().first()
        if not row or not row.open_ai_key:
            return None
        try:
            return decrypt_text(row.open_ai_key)
        except Exception:
            return None

    async def load_api_key(self):
        if self.chat is not None:
            return

        api_key = await self._fetch_plain_key()

        if not api_key:
            raise RuntimeError("OPENAI API key not set in settings or DB")

        os.environ["OPENAI_API_KEY"] = api_key
        self.chat = ChatOpenAI(model_name="gpt-5-mini", temperature=0.2)

    async def llm_chat(self, message: str) -> str:
        await self.load_api_key()

        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=message)]
        try:
            resp = await self.chat.agenerate([[messages[0], messages[1]]])
            text = resp.generations[0][0].text
        except Exception as e:
            return BuildJSONResponses.raise_exception(str(e))
        return BuildJSONResponses.success_response(text, "LLM chat response")
    
    async def save_llm_key(self, message: str) -> str:
        try:
            encrypted = encrypt_text(message)
            data = self.model(
                open_ai_key=encrypted
            )
            self.db.add(data)
            await self.db.commit()
            await self.db.refresh(data)
            return BuildJSONResponses.success_response(
                None, "Key Added Successfully"
            )

        except Exception as e:
            return BuildJSONResponses.raise_exception(str(e))

    async def get_llm_key(self) -> str:
        try:
            result = await self.db.execute(select(self.model))
            row = result.scalars().first()
            if not row or not row.open_ai_key:
                return BuildJSONResponses.raise_exception("No LLM key found")
            try:
                decrypted = decrypt_text(row.open_ai_key)
            except Exception as e:
                return BuildJSONResponses.raise_exception(f"Decryption failed: {e}")
            return BuildJSONResponses.success_response(decrypted, "Key fetched successfully")
        except Exception as e:
            return BuildJSONResponses.raise_exception(str(e))