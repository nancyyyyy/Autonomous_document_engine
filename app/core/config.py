from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous Documentation Engine"
    API_V1_STR: str = "/api/v1"
    
    # Database - Using SQLite for now
    DATABASE_URL: str = "sqlite:///./ade.db"
    
    # Redis (will be used later)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # GitHub
    GITHUB_WEBHOOK_SECRET: str = "change-this-to-a-strong-secret"
    GITHUB_APP_ID: str = ""
    GITHUB_PRIVATE_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()