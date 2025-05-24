import os
from typing import List, Dict, Any, Optional
from mistralai import Mistral
from mistralai.models import UserMessage, SystemMessage, AssistantMessage

from app.core.config import MISTRAL_API_KEY, MISTRAL_MODEL

class MistralService:
    """
    Service to handle interactions with the Mistral AI API.
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the Mistral client.
        
        Args:
            api_key: Optional API key. If not provided, uses the one from environment variables.
            model: Optional model name. If not provided, uses the default from config.
        """
        self.api_key = api_key or MISTRAL_API_KEY
        if not self.api_key:
            raise ValueError("Mistral API key must be provided or set in environment variables")
            
        self.default_model = model or MISTRAL_MODEL
        self.client = Mistral(api_key=self.api_key)
    
    def complete(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None
    ) -> str:
        """
        Generate a completion from the given messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            model: Optional model name to use. Defaults to the instance default.
            temperature: Controls randomness. Higher values mean more creative responses.
            max_tokens: Maximum number of tokens to generate.
            top_p: Controls diversity via nucleus sampling.
            random_seed: Optional seed for deterministic outputs.
            
        Returns:
            The generated text completion.
        """
        # Convert dict messages to ChatMessage objects if needed
        chat_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                chat_messages.append({"role": role, "content": content})
            else:
                chat_messages.append(msg)
        
        response = self.client.chat.complete(
            model=model or self.default_model,
            messages=chat_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            random_seed=random_seed
        )
        
        return response.choices[0].message.content
    
    def generate_embeddings(self, texts: List[str], model: str = "mistral-embed") -> List[List[float]]:
        """
        Generate embeddings for the provided texts.
        
        Args:
            texts: List of text strings to embed.
            model: Model to use for embeddings, defaults to mistral-embed.
            
        Returns:
            List of embedding vectors.
        """
        response = self.client.embeddings.create(
            model=model,
            inputs=texts
        )
        
        # Extract embeddings from response
        embeddings = [item.embedding for item in response.data]
        return embeddings

# Create a singleton instance for easy import
mistral_service = MistralService()

def get_completion(
    prompt: str, 
    system_prompt: str = None, 
    model: str = None, 
    temperature: float = 0.7
) -> str:
    """
    Helper function to get a completion for a single user prompt.
    
    Args:
        prompt: The user's prompt text.
        system_prompt: Optional system instructions.
        model: Optional model name.
        temperature: Controls randomness of output.
        
    Returns:
        Generated completion text.
    """
    messages = []
    
    # Add system message if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add user message
    messages.append({"role": "user", "content": prompt})
    
    return mistral_service.complete(
        messages=messages,
        model=model,
        temperature=temperature
    )