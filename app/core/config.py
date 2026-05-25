from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous Documentation Engine"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "ade_db"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str
    
    GITHUB_WEBHOOK_SECRET: str
    GITHUB_APP_ID: str
    GITHUB_PRIVATE_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()