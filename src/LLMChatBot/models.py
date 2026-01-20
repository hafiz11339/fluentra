from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP, func, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class LLMKeys(Base):
    __tablename__ = "LLM_keys"
    id = Column(Integer, primary_key=True,autoincrement=True)
    open_ai_key = Column(String(220), nullable=True)
