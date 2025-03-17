from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class AppMode(str, Enum):
    HTTP = "http"
    QUEUE = "queue"


class Settings(BaseSettings):
    APP_MODE: AppMode = Field(default=AppMode.HTTP, env="APP_MODE")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="kafka:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC: str = Field(default="audio_transcription", env="KAFKA_TOPIC")

    REDIS_HOST: str = Field(default="redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
