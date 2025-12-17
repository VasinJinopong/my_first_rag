from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base
import uuid 



class Document(Base):
    """Document metadata model"""
    
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    title = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    file_name = Column(String(255),nullable=False)
    file_path = Column(String(512),nullable=False)
    file_size = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=False)
    chunk_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title})>"