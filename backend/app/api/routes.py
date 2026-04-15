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
    
    Full workflow:
    1. Split story into scenes
    2. Generate image prompts for each scene
    3. Generate images for each scene
    4. Return complete storyboard with images and narration
    """
    from ..services.ollama_service import OllamaService
    from ..services.image_service import ImageService
    
    if not request.story or not request.story.strip():
        raise HTTPException(status_code=400, detail="Story text is required")
    
    try:
        # Initialize services
        ollama_service = OllamaService()
        image_service = ImageService()
        
        # Step 1: Split story into scenes
        print(f"Splitting story into scenes...")
        scenes = await ollama_service.split_story_into_scenes(
            request.story, 
            num_scenes=request.num_scenes
        )
        
        if not scenes:
            raise HTTPException(
                status_code=500, 
                detail="Failed to split story into scenes"
            )
        
        print(f"Created {len(scenes)} scenes")
        
        # Step 2: Process each scene (generate image prompt and image)
        storyboard = []
        for i, scene in enumerate(scenes):
            scene_number = scene.get("scene_number", i + 1)
            description = scene.get("description", "")
            narration = scene.get("narration", "")
            
            print(f"Processing scene {scene_number}...")
            
            # Generate image prompt from scene description
            image_prompt = None
            image_url = None
            
            if description:
                try:
                    print(f"Generating image prompt for scene {scene_number}...")
                    image_prompt = await ollama_service.generate_image_prompt(description)
                    
                    if image_prompt:
                        print(f"Generating image for scene {scene_number}...")
                        image_url = await image_service.generate_and_save_image(image_prompt)
                        if not image_url:
                            print(f"Warning: Image generation failed for scene {scene_number}")
                    else:
                        print(f"Warning: Image prompt generation failed for scene {scene_number}")
                except Exception as e:
                    print(f"Error processing image for scene {scene_number}: {str(e)}")
                    # Continue without image if generation fails
            
            storyboard.append(SceneResponse(
                scene_number=scene_number,
                description=description,
                narration=narration,
                image_url=image_url
            ))
        
        print(f"Storyboard generation complete with {len(storyboard)} scenes")
        return storyboard

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating storyboard: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate storyboard: {str(e)}"
        )


@router.get("/test-ollama")
async def test_ollama():
    """
    Test endpoint to verify Ollama connection
    """
    from ..services.ollama_service import OllamaService
    
    try:
        ollama_service = OllamaService()
        # Test with a simple prompt
        response = await ollama_service.generate_text("Say 'Hello, Ollama is working!' if you can read this.")
        return {
            "status": "success",
            "message": "Ollama connection successful",
            "test_response": response[:100] if response else "No response",
            "model": ollama_service.model,
            "base_url": ollama_service.base_url
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama connection failed: {str(e)}"
        )

