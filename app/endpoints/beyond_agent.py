from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database.setup import get_db
from app.database.models import get_student_data
from app.services.beyond_service import beyond_service
from app.services.mistral_service import get_completion

router = APIRouter()

class AgentRequest(BaseModel):
    student_id: int
    name: Optional[str] = None
    avatar_id: Optional[str] = None
    language: Optional[str] = "en"

class AgentResponse(BaseModel):
    agent_id: str
    embed_code: str

@router.post("/create", response_model=AgentResponse)
async def create_agent(request: AgentRequest, db: Session = Depends(get_db)):
    """
    Create a Beyond Presence agent with student context.
    """
    try:
        # Get student data from database
        student_data = get_student_data(db, request.student_id)
        
        if "error" in student_data:
            raise HTTPException(status_code=404, detail=student_data["error"])
            
        # Use Mistral to condense and prepare the student data for the agent context
        context_prompt = f"""
        Analyze this student's quiz data and provide a concise summary that highlights strengths, 
        weaknesses, and learning patterns. This will be used to personalize an educational AI agent.
        Student data: {student_data}
        """
        
        student_context = get_completion(
            prompt=context_prompt,
            system_prompt="You are an educational analyst that synthesizes student data into actionable insights.",
            temperature=0.3
        )
        
        # Create the system prompt for the agent with the student context
        agent_system_prompt = f"""
        You are a personalized educational assistant for {student_data['student_name']}.
        
        Here's what you know about this student's performance:
        {student_context}
        
        Your role is to:
        1. Provide personalized tutoring based on the student's identified strengths and weaknesses
        2. Adapt your teaching style to the student's learning patterns
        3. Offer encouragement focused on areas where the student has struggled
        4. Challenge the student further in subjects where they excel
        5. Be friendly, patient, and engaging
        
        Maintain this context throughout your conversation with the student.
        """
        
        # Use the student's name if no custom name is provided
        agent_name = request.name or f"{student_data['student_name']}'s Educational Assistant"
        
        # Create the agent
        agent_result = beyond_service.create_agent(
            system_prompt=agent_system_prompt,
            name=agent_name,
            language=request.language,
            avatar_id=request.avatar_id
        )
        
        # Get the embed code
        embed_code = beyond_service.get_embed_code(agent_result['id'])
        
        return {
            "agent_id": agent_result['id'],
            "embed_code": embed_code
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")