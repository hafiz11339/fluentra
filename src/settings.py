from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
from typing import Set


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI AI BE"
    VERSION: str = "1.1"
    DOCS_URL: str = "/docs"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8181
    ENVIRONMET: str = "dev"
    SCHEMA_NAME: str = "public"
    ALLOWED_HOSTS: Set[str] = {"*"}
    DATABASE_URL: str
    ENCRYPTION_KEY: Optional[str] = None
    class Config:
        env_file = ".env"

    @property
    def fastapi_kwargs(self):
        return {
            "docs_url": self.DOCS_URL,
            "title": self.PROJECT_NAME,
            "version": self.VERSION,
        }


settings = Settings()
