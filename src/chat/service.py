from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import json
import time

from src.chat.models import ChatHistory
from src.chat.schemas import SourceChunk, AnswerResponse
from src.vector_store.client import vector_store
from src.core.config import get_settings
from src.core.logging import logger, log_performance

settings = get_settings()

class ChatService:
    """Service for chat/Q&A operations"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_CHAT_MODEL,
            temperature=0,
            openai_api_key =settings.OPENAI_API_KEY
        )
        
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are a helpful AI assisstant that answer question based on provided context
                 
                 Instructions:
                 1. Answer using ONLY the information from the provided context
                 2. If the context doesn't contain enough information, say "I don't have enough information to answer this question based on the provided documents
                 3. Be concise and direct
                 4. If you quote from context, indicate with source
                 5. If multiple sources provide information, synthesize them coherently
                 
                 Context:
                 {context}
                 """),
                
                ("human", "{question}")
            ]
        )
        
    def search_similar(self, query:str, k:int=3, document_ids : Optional[List[str]]= None) -> List[tuple]:
        """Search for similar chunks"""
        start_time = time.time()
        
        filter_dict = None
        if document_ids:
            filter_dict = {"document_id": {"$in": document_ids}}
        
        results = vector_store.search_similar(query=query, k=k, filter_dict=filter_dict)
        
        log_performance("search_similarity", time.time() - start_time, k=k)
        return results  
    
    def generate_answer(self, question:str, context: str) -> str:
        """Generate answer using LLM"""
        start_time = time.time()
        
        messages = self.qa_prompt.format_messages(context=context, question= question)
        response = self.llm.invoke(messages)
        answer = response.content
        
        log_performance("generate_answer", time.time() - start_time)
        return answer
    
    
    def assess_confidence(self,answer:str , sources_count: int) -> str:
        """Assess confidence level"""
        if "don't have enough information" in answer.lower():
            return "low"
        elif sources_count >= 3:
            return "high"
        elif sources_count >= 2:
            return "medium"
        
        else:
            return "low"
        
        
    def save_chat(self, question:str, answer: str, confidence: str, top_k: int, document_ids : Optional[List[str]], db:Session) -> ChatHistory:
        """Save chat to history"""
        chat = ChatHistory(
            question= question,
            answer = answer,
            confidence = confidence,
            top_k= top_k,
            document_ids=json.dumps(document_ids) if document_ids else None
            
        )
        
        db.add(chat)
        db.commit()
        db.refresh(chat)
        
        logger.info(f"Chat saved: {chat.id}")
        return chat
    
    def ask_question(self, question:str, document_ids: Optional[List[str]], top_k:int, db:Session )-> AnswerResponse:
        """Main RAG workflow"""
        
        start_time = time.time()
        
        search_results = self.search_similar(query=question, k=top_k, document_ids=document_ids)
        
        sources = []
        context_parts = []
        
        for doc,score in search_results:
            source = SourceChunk(
                document_id = doc.metadata.get("document_id", ""),
                document_title=doc.metadata.get("title","Unknown"),
                chunk_index= doc.metadata.get("chunk_index"),
                content= doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                similarity_score=float(score)
            )
            sources.append(source)
            context_parts.append(f"[Source: {doc.metadata.get('title','Unknown')}]\n{doc.page_content}")
        
        context = "\n\n---\n\n".join(context_parts)    
            
        if not context_parts:
            answer = "I couldn't find any. relevant information in the documents to answer your question."
            confidence = "low"
            
        else:
            answer = self.generate_answer(question, context)
            confidence = self.assess_confidence(answer, len(sources))
            
        chat = self.save_chat(question,answer, confidence, top_k, document_ids, db)
        
        log_performance("ask_question", time.time() - start_time)
        
        return AnswerResponse(
            id = chat.id,
            question = question,
            answer = answer,
            sources= sources,
            confidence = confidence,
            created_at = chat.created_at
        )
        
    def get_chat_history(self, db:Session, limit: int = 50) -> List[ChatHistory]:
        """Get recent chat history"""
        return db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    
chat_service = ChatService()