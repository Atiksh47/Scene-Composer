"""
Ollama service for LLM operations
"""
import httpx
import os
from typing import Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")


class OllamaService:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL
    
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated text response
        """
        # TODO: Implement Ollama API call
        pass
    
    async def split_story_into_scenes(self, story: str) -> list[dict]:
        """
        Split a story into scenes using LLM
        
        Args:
            story: Full story text
            
        Returns:
            List of scene dictionaries with description and narration
        """
        # TODO: Implement story splitting logic
        pass
    
    async def generate_image_prompt(self, scene_description: str) -> str:
        """
        Generate an image generation prompt from scene description
        
        Args:
            scene_description: Description of the scene
            
        Returns:
            Detailed image generation prompt
        """
        # TODO: Implement prompt generation
        pass

