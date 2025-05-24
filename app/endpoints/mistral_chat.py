from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.mistral_service import get_completion, mistral_service

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    model: Optional[str] = None

class EmbeddingRequest(BaseModel):
    texts: List[str]
    model: Optional[str] = "mistral-embed"

@router.post("/chat")
async def chat_completion(request: ChatRequest):
    """
    Generate a response from Mistral API based on the provided prompt.
    """
    try:
        response = get_completion(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            model=request.model
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Mistral API: {str(e)}")

@router.post("/embeddings")
async def generate_embeddings(request: EmbeddingRequest):
    """
    Generate embeddings for the provided texts using Mistral API.
    """
    try:
        embeddings = mistral_service.generate_embeddings(
            texts=request.texts,
            model=request.model
        )
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")