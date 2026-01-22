from sqlalchemy import Column, Integer, String, Text, JSON, BigInteger, func, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class LLMKeys(Base):
    __tablename__ = "LLM_keys"
    id = Column(Integer, primary_key=True,autoincrement=True)
    open_ai_key = Column(String(220), nullable=True)



class ChatHistory(Base):
    __tablename__ = "chat_history"  # change if your table name is different

    id = Column(BigInteger, primary_key=True, index=True)
    quest = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    created_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True
    )
    session_id = Column(BigInteger, nullable=True)