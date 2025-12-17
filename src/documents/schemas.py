from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentUpload(BaseModel):
    """Schema for document upload"""
    title: str = Field(...,min_length=1,max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
class DocumentResponse(BaseModel):
    """Schema for document response"""
    id:str
    title:str
    description : Optional[str]
    file_name:str
    file_size:int
    page_count: int
    chunk_count:int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class DocumentStats(BaseModel):
    """Schema for indexing statistics"""
    document_id: str
    chunks_created:int
    text_length: int
    processing_time: float
    
    
class VectorStoreStats(BaseModel):
    """Schema for vector store statistics"""
    collection_name: str
    total_documents: int
    persist_directory:str