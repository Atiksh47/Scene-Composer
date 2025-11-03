# Setup Guide

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Copy the example file (you'll need to create .env manually on Windows)
# Windows PowerShell:
Copy-Item env.example .env
# Or manually create .env with the contents from env.example

# Run the server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 2. Ollama Setup

Make sure Ollama is running:

```bash
# Check if Ollama is running
ollama list

# If not installed, download from https://ollama.ai
# Pull a model (recommended for CPU: llama2 or mistral)
ollama pull llama2
# or
ollama pull mistral
```

Update `backend/.env` with your chosen model:
```
OLLAMA_MODEL=llama2
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Verify Setup

1. **Backend**: Visit `http://localhost:8000` - should see API info
2. **Backend Health**: Visit `http://localhost:8000/health` - should return `{"status": "healthy"}`
3. **Frontend**: Visit `http://localhost:5173` - should see the app interface

## Next Steps

Once everything is set up, we'll implement:
1. Ollama service integration
2. Image generation service
3. Story splitting logic
4. Frontend storyboard display

