from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List, Dict, Any

from app.database.setup import Base

class QuizData(Base):
    """
    SQLAlchemy model for the quiz_data table.
    """
    __tablename__ = "quiz_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(Text, nullable=False)
    quiz_id = Column(Text, nullable=False)
    question_number = Column(Integer, nullable=False)
    course = Column(Text, nullable=False)
    subject = Column(Text, nullable=False)
    sub_subject = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    expected_response = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    is_correct_answer = Column(Boolean, nullable=False, default=False)
    difficulty = Column(Text, nullable=False)
    time_spent = Column(Integer, nullable=False)  # in seconds
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


def get_student_data(db: Session, student_id: str) -> Dict[str, Any]:
    """
    Retrieve and organize quiz data for a specific student.
    
    Args:
        db: Database session
        student_id: Student user ID
        
    Returns:
        Dictionary containing organized student data
    """
    # Query for the student's quiz data
    quiz_data = db.query(QuizData).filter(QuizData.user_id == student_id).all()
    
    if not quiz_data:
        return {"error": f"No data found for student ID {student_id}"}
    
    # Organize by subject and sub_subject
    subjects = {}
    for entry in quiz_data:
        if entry.subject not in subjects:
            subjects[entry.subject] = {}
            
        if entry.sub_subject not in subjects[entry.subject]:
            subjects[entry.subject][entry.sub_subject] = {
                "correct": 0,
                "incorrect": 0,
                "total": 0,
                "avg_time": 0,
                "total_time": 0,
                "questions": []
            }
        
        subj_data = subjects[entry.subject][entry.sub_subject]
        subj_data["total"] += 1
        subj_data["total_time"] += entry.time_spent
        
        if entry.is_correct_answer:
            subj_data["correct"] += 1
        else:
            subj_data["incorrect"] += 1
            
        # Add question details
        subj_data["questions"].append({
            "question": entry.question,
            "expected_response": entry.expected_response,
            "student_response": entry.response,
            "is_correct": entry.is_correct_answer,
            "difficulty": entry.difficulty,
            "time_spent": entry.time_spent
        })
    
    # Calculate averages for each sub_subject
    for subject, sub_subjects in subjects.items():
        for sub_name, sub_data in sub_subjects.items():
            if sub_data["total"] > 0:
                sub_data["avg_time"] = sub_data["total_time"] / sub_data["total"]
    
    return {
        "student_id": student_id,
        "subjects": subjects
    }