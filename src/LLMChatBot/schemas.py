from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str
    session_id: int
    
    
class LLMKeyData(BaseModel):
    key: str