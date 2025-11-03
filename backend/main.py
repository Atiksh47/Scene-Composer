"""
FastAPI backend for AI Scene Composer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="AI Scene Composer API", version="1.0.0")

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Scene Composer API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Include API routes
from app.api.routes import router as api_router
app.include_router(api_router, prefix="/api", tags=["storyboard"])

