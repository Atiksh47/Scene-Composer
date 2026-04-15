"""
Ollama service for LLM operations
"""
import httpx
import os
from typing import Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")


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
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False  # Disable extended reasoning for faster responses
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
            except httpx.RequestError as e:
                raise Exception(f"Failed to connect to Ollama: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Ollama API error: {e.response.status_code} - {e.response.text}")
    
    async def split_story_into_scenes(self, story: str, num_scenes: Optional[int] = None) -> list[dict]:
        """
        Split a story into scenes using LLM
        
        Args:
            story: Full story text
            num_scenes: Optional number of scenes to create
            
        Returns:
            List of scene dictionaries with description and narration
        """
        system_prompt = """You are a storyboard assistant. Your task is to split stories into scenes.
For each scene, provide:
1. A brief visual description (what would be shown in an image)
2. A narration text (what would be narrated over the scene)

Format your response as a JSON array of objects, where each object has:
- "scene_number": integer (starting from 1)
- "description": string (visual description for image generation)
- "narration": string (narrated text for the scene)

Be concise but descriptive. Return ONLY the JSON array, no other text."""

        user_prompt = f"""Split the following story into scenes. 
{f'Create exactly {num_scenes} scenes.' if num_scenes else 'Determine an appropriate number of scenes based on the story structure.'}

Story:
{story}

Return a JSON array of scene objects with scene_number, description, and narration fields."""

        response_text = await self.generate_text(user_prompt, system_prompt)

        import json
        import re

        # Strip markdown code fences (```json ... ``` or ``` ... ```)
        cleaned = re.sub(r'```(?:json)?\s*', '', response_text)
        cleaned = re.sub(r'```', '', cleaned).strip()

        # Try to find a JSON array anywhere in the (cleaned) response
        json_match = re.search(r'\[.*\]', cleaned, re.DOTALL)
        if json_match:
            try:
                scenes = json.loads(json_match.group())
                result = []
                for i, scene in enumerate(scenes, 1):
                    if isinstance(scene, dict):
                        result.append({
                            "scene_number": scene.get("scene_number", i),
                            "description": scene.get("description", "").strip(),
                            "narration": scene.get("narration", "").strip()
                        })
                if result:
                    return result
            except json.JSONDecodeError:
                pass

        # Fallback: create a single scene from the story
        print("Warning: Could not parse JSON scenes from model response, using fallback.")
        return [{
            "scene_number": 1,
            "description": story[:200] + "..." if len(story) > 200 else story,
            "narration": story[:150] + "..." if len(story) > 150 else story
        }]
    
    async def generate_image_prompt(self, scene_description: str) -> str:
        """
        Generate an image generation prompt from scene description
        
        Args:
            scene_description: Description of the scene
            
        Returns:
            Detailed image generation prompt
        """
        system_prompt = """You are an image prompt generator. Convert scene descriptions into detailed, 
vivid image generation prompts that will produce high-quality illustrations. Include:
- Visual details (characters, setting, objects)
- Composition and framing
- Style and mood
- Lighting and atmosphere

Be specific and descriptive. Return ONLY the prompt text, no explanations."""

        user_prompt = f"""Convert this scene description into a detailed image generation prompt:

{scene_description}

Generate a vivid, detailed prompt for text-to-image generation."""

        prompt = await self.generate_text(user_prompt, system_prompt)
        # Clean up the prompt and ensure it's well-formatted
        return prompt.strip()

