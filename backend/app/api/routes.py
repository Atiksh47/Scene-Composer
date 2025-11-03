"""
API routes for scene composer
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class StoryRequest(BaseModel):
    story: str
    num_scenes: Optional[int] = None


class SceneResponse(BaseModel):
    scene_number: int
    description: str
    narration: str
    image_url: Optional[str] = None


@router.post("/generate-storyboard", response_model=List[SceneResponse])
async def generate_storyboard(request: StoryRequest):
    """
    Generate a storyboard from a story description
    
    TODO: Implement full workflow:
    1. Split story into scenes
    2. Generate image prompts
    3. Generate images
    4. Generate narration
    5. Return storyboard
    """
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/test-ollama")
async def test_ollama():
    """
    Test endpoint to verify Ollama connection
    """
    # TODO: Implement Ollama connection test
    return {"status": "test endpoint - not implemented"}

