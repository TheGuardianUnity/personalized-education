import os
import requests
from typing import List, Dict, Any, Optional

from app.core.config import BEY_API_KEY

class BeyondService:
    """
    Service to handle interactions with the Beyond Presence API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Beyond Presence client.
        
        Args:
            api_key: Optional API key. If not provided, uses the one from environment variables.
        """
        self.api_key = api_key or BEY_API_KEY
        if not self.api_key:
            raise ValueError("Beyond Presence API key must be provided or set in environment variables")
        
        self.base_url = "https://api.bey.dev/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def create_agent(
        self, 
        system_prompt: str, 
        name: str = "Education Assistant",
        language: str = "en",
        greeting: str = "Hello! I'm your educational assistant.",
        max_session_length_minutes: int = 30,
        capabilities: List[str] = ["webcam_vision"],
        avatar_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new Beyond Presence agent.
        
        Args:
            system_prompt: Instructions for the agent.
            name: Name of the agent.
            language: Language code for the agent.
            greeting: Initial greeting from the agent.
            max_session_length_minutes: Maximum session length.
            capabilities: List of capabilities for the agent.
            avatar_id: Optional avatar ID.
            
        Returns:
            The agent data including the agent ID.
        """
        endpoint = f"{self.base_url}/agent"
        
        payload = {
            "system_prompt": system_prompt,
            "name": name,
            "language": language,
            "greeting": greeting,
            "max_session_length_minutes": max_session_length_minutes,
            "capabilities": capabilities
        }
        
        if avatar_id:
            payload["avatar_id"] = avatar_id
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        return response.json()
    
    def get_embed_code(self, agent_id: str) -> str:
        """
        Generate an embed code for the agent.
        
        Args:
            agent_id: The ID of the agent.
            
        Returns:
            HTML iframe code for embedding the agent.
        """
        iframe_code = f"""<iframe 
    src="https://bey.chat/{agent_id}" 
    width="100%" 
    height="600px" 
    frameborder="0" 
    allowfullscreen
    allow="camera; microphone; fullscreen"
    style="border: none; max-width: 100%;"
></iframe>"""
        return iframe_code

# Create a singleton instance for easy import
beyond_service = BeyondService()