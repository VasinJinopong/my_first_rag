import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import Optional, List, Dict
from src.core.config import get_settings
from src.core.logging import logger
import os

settings = get_settings()

class VectorStoreClient:
    """Client for ChromaDB vector store operations"""
    
    def __init__(self):
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key = settings.OPENAI_API_KEY
        )
        
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"description": "Document embeddings for RAG"}
        )
        
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function = self.embeddings
        )
        
        logger.info(f"Vector store initialized: {settings.CHROMA_COLLECTION_NAME}")
        
    def add_documents(self, texts: List[str], metadatas:List[Dict], ids:Optional[List[str]]= None) -> List[str]:
        """Add documents to vector store"""
        try:
            doc_ids = self.vectorstore.add_texts(texts=texts, metadatas=metadatas,ids = ids)
            logger.info(f"Added {len(doc_ids)} documents to vector store")
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise
        
    def search_similar(self,query:str , k:int = 3, filter_dict:Optional[Dict]= None):
        """Search for similarity documents"""
        try:
            results = self.vectorstore.similarity_search_with_score(query=query,k=k, filter=filter_dict)
            logger.info(f"Search return {len(results)} results")   
            return results 
            
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
    
    def delete_by_document_id(self,document_id:str):
        """Delete all chuck for a document"""
        try:
            results = self.collection.get(where={"document_id": document_id})
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise
    
    def get_stats(self)-> Dict:
        """Get collection statistics"""
        count = self.collection.count()
        return {
            "collection_name" : settings.CHROMA_COLLECTION_NAME,
            "total_documents": count,
            "persist_directory" : settings.CHROMA_PERSIST_DIR
        }


vector_store = VectorStoreClient()