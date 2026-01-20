from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str
    
    
class LLMKeyData(BaseModel):
    key: str