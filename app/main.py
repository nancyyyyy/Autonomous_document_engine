from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1.endpoints.webhooks import router as webhooks_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 ADE Backend Starting...")
    create_db_and_tables()          # Force database creation
    print("🚀 ADE Backend Started Successfully!")
    print("📡 API Docs available at: http://localhost:8000/docs")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(webhooks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 Autonomous Documentation Engine is LIVE!",
        "status": "healthy",
        "database": "SQLite (Temporary)"
    }