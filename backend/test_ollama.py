import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")

async def test():
    print(f"Testing Ollama at {OLLAMA_BASE_URL} with model '{OLLAMA_MODEL}'...")
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            r = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": "hello", "stream": False}
            )
            print(f"Status: {r.status_code}")
            print(f"Response: {r.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test())
