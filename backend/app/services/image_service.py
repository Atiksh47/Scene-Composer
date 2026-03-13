"""
Image generation service
Will integrate with free text-to-image APIs
"""
import httpx
import os
import uuid
from typing import Optional
from pathlib import Path

# Using Hugging Face Inference API with a free text-to-image model
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "stabilityai/stable-diffusion-2-1")
HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

# Image storage directory
IMAGES_DIR = Path(__file__).parent.parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)


class ImageService:
    def __init__(self):
        self.api_key = HUGGINGFACE_API_KEY
        self.api_url = HUGGINGFACE_API_URL
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        self.images_dir = IMAGES_DIR
    
    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """
        Generate an image from a text prompt using Hugging Face Inference API
        
        Args:
            prompt: Image generation prompt
            
        Returns:
            Image bytes (PNG/JPEG) or None if failed
        """
        if not prompt or not prompt.strip():
            return None
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": prompt.strip()}
                )
                
                # Handle rate limiting (model loading)
                if response.status_code == 503:
                    # Model might be loading, wait and retry once
                    import asyncio
                    await asyncio.sleep(5)
                    response = await client.post(
                        self.api_url,
                        headers=self.headers,
                        json={"inputs": prompt.strip()}
                    )
                
                response.raise_for_status()
                
                # Check if response is image bytes
                content_type = response.headers.get("content-type", "")
                if "image" in content_type:
                    return response.content
                else:
                    # Might be JSON error response
                    try:
                        error_data = response.json()
                        print(f"Hugging Face API error: {error_data}")
                        return None
                    except:
                        return None
                        
            except httpx.TimeoutException:
                print("Image generation timeout")
                return None
            except httpx.RequestError as e:
                print(f"Failed to connect to Hugging Face API: {str(e)}")
                return None
            except httpx.HTTPStatusError as e:
                print(f"Hugging Face API error: {e.response.status_code}")
                return None
            except Exception as e:
                print(f"Unexpected error in image generation: {str(e)}")
                return None
    
    async def generate_and_save_image(self, prompt: str) -> Optional[str]:
        """
        Generate an image and save it to disk, returning the URL path
        
        Args:
            prompt: Image generation prompt
            
        Returns:
            URL path to the saved image (e.g., "/api/images/abc123.png") or None if failed
        """
        image_bytes = await self.generate_image(prompt)
        if not image_bytes:
            return None
        
        # Generate unique filename
        image_id = str(uuid.uuid4())
        image_path = self.images_dir / f"{image_id}.png"
        
        try:
            # Save image to disk
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            # Return URL path
            return f"/api/images/{image_id}.png"
        except Exception as e:
            print(f"Failed to save image: {str(e)}")
            return None

