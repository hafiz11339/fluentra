from dotenv import load_dotenv
import os
from src.settings import settings
from src.response import BuildJSONResponses
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.LLMChatBot.prompt import SYSTEM_PROMPT
from src.LLMChatBot.models import LLMKeys
from src.LLMChatBot.models import ChatHistory
from src.LLMChatBot.utils import encrypt_text, decrypt_text
from sqlalchemy import select
from typing import Optional

class ChatService:
    def __init__(self, db):
        self.db = db
        self.model = LLMKeys
        self.chat: Optional[ChatOpenAI] = None
        self.MAX_ASSISTANT_CHARS = 1000


    async def _fetch_plain_key(self):
        result = await self.db.execute(select(self.model).where(self.model.id == 7))

        row = result.scalars().first()
        if not row or not row.open_ai_key:
            return None
        try:
            return decrypt_text(row.open_ai_key)
        except Exception:
            return None

    async def load_api_key(self):

        os.environ["OPENAI_API_KEY"] = settings.OPENAI_KEY
        self.chat = ChatOpenAI(model_name=settings.OPEN_AI_MODEL, temperature=settings.OPEN_AI_TEMPERATURE)

    async def llm_chat(self, message: str, session_id: int) -> str:
        await self.load_api_key()

        # Fetch last 5 chat history entries for this session ordered by date
        try:
            q = select(ChatHistory).where(ChatHistory.session_id == session_id).order_by(ChatHistory.created_date.desc()).limit(5)
            result = await self.db.execute(q)
            rows = result.scalars().all() or []
        except Exception as e:
            print("Error fetching chat history:", e)
            return BuildJSONResponses.raise_exception(str(e))

        # Rebuild conversation in chronological order (oldest first)
        rows = list(reversed(rows))
        messages = []

        if not rows:
            messages.append(
                SystemMessage(
                    content=SYSTEM_PROMPT
                    + "\n\nAssume this is the start of a new conversation. Gently ground the user."
                )
            )
        else:
            messages.append(SystemMessage(content=SYSTEM_PROMPT))

        for row in rows:
            if row.quest:
                messages.append(HumanMessage(content=row.quest))
            if row.answer:
                messages.append(AIMessage(content=row.answer[:self.MAX_ASSISTANT_CHARS]))

        # Add current user message
        messages.append(HumanMessage(content=message))

        try:
            # langchain's agenerate expects a list of message lists for batch generation
            resp = await self.chat.agenerate([messages])
            text = resp.generations[0][0].text
        except Exception as e:
            print("Error during LLM chat:", e)
            return BuildJSONResponses.raise_exception(str(e))

        # Save the new exchange into chat_history
        try:
            entry = ChatHistory(quest=message, answer=text, session_id=session_id)
            self.db.add(entry)
            await self.db.commit()
            await self.db.refresh(entry)
        except Exception as e:
            print("Warning: failed to save chat history:", e)

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
        
    async def get_latest_id(self) -> str:
        try:
            result = await self.db.execute(
                select(ChatHistory.session_id).order_by(ChatHistory.session_id.desc()).limit(1)
            )
            row = result.scalars().first()
            if not row:
                next_session_id = 1
            else:
                try:
                    next_session_id = int(row) + 1
                except Exception:
                    return BuildJSONResponses.raise_exception("Invalid session id in DB")
            return BuildJSONResponses.success_response(next_session_id, "Next session ID generated successfully")
        except Exception as e:
            return BuildJSONResponses.raise_exception(str(e))