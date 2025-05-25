from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.setup import Base

class QuizResponses(Base):
    __tablename__ = "quiz_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    quiz_id = Column(String, nullable=False)
    question_number = Column(Integer, nullable=False)
    course = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    sub_subject = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text)
    expected_response = Column(Text, nullable=False)
    is_correct_answer = Column(Boolean, default=False)
    difficulty = Column(String, nullable=False)
    time_spent = Column(Integer)
    created_at = Column(DateTime, server_default=text('now()'))