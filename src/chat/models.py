from sqlalchemy import Column, String, Text, DateTime, Float
from sqlalchemy.sql import func
from src.database import Base
import uuid


class ChatHistory(Base):
    """Chat history model"""
    
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence = Column(String(20), nullable=True)
    
    top_k = Column(Float,default=3)
    document_ids = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, question={self.question[:50]}...)>"