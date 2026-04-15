"""
FastAPI backend for AI Scene Composer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI(title="AI Scene Composer API", version="1.0.0")

# Create images directory if it doesn't exist
images_dir = Path(__file__).parent / "images"
images_dir.mkdir(exist_ok=True)

# Mount static files for serving images
app.mount("/api/images", StaticFiles(directory=str(images_dir)), name="images")

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

