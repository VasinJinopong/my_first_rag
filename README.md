
markdown# 📄 Document Q&A API (RAG)

A production-ready RAG (Retrieval-Augmented Generation) system for document question-answering using FastAPI, LangChain, OpenAI, and ChromaDB.

## 🎯 Features

- **Document Upload**: Support PDF, DOCX, TXT files
- **Intelligent Q&A**: Ask questions and get AI-powered answers from your documents
- **Vector Search**: Semantic search using ChromaDB and OpenAI embeddings
- **Source Citations**: Every answer includes relevant source chunks
- **Chat History**: Track all questions and answers
- **REST API**: Clean FastAPI endpoints with auto-documentation

## 🏗️ Architecture
```
User Question → Vectorize → Search ChromaDB → Retrieve Chunks → 
Send to GPT with Context → Generate Answer → Return with Sources
```

## 📁 Project Structure
```
document-qa/
├── src/
│   ├── core/                 # Core configurations
│   │   ├── config.py        # Settings
│   │   └── logging.py       # Logging
│   ├── database.py          # SQLAlchemy setup
│   ├── vector_store/        # ChromaDB integration
│   │   └── client.py
│   ├── documents/           # Document management
│   │   ├── models.py        # DB models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── router.py        # API endpoints
│   │   └── service.py       # Business logic
│   ├── chat/                # Q&A functionality
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── router.py
│   │   └── service.py       # RAG logic
│   └── main.py              # FastAPI app
├── docker-compose.yml       # PostgreSQL
├── requirements.txt
└── .env
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/document-qa.git
cd document-qa
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create `.env` file:
```bash
DATABASE_URL=postgresql://doc_user:doc_password@localhost:5432/doc_db
OPENAI_API_KEY=your-openai-api-key
DEBUG=True
```

### 5. Start PostgreSQL
```bash
docker-compose up -d
```

### 6. Run the API
```bash
python -m src.main
```

API will be available at: http://localhost:8000

Documentation: http://localhost:8000/docs

## 📝 API Usage

### Upload a Document
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  -F "description=Optional description"
```

### Ask a Question
```bash
curl -X POST "http://localhost:8000/api/v1/chat/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "id": "...",
  "question": "What is the main topic?",
  "answer": "The main topic is...",
  "sources": [
    {
      "document_title": "My Document",
      "content": "...",
      "similarity_score": 0.89
    }
  ],
  "confidence": "high"
}
```

### Get Chat History
```bash
curl http://localhost:8000/api/v1/chat/history
```

### Get Stats
```bash
curl http://localhost:8000/api/v1/documents/stats
```

## 🔧 Configuration

Edit `.env` to customize:
```bash
# OpenAI
OPENAI_API_KEY=your-key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-3.5-turbo

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database for metadata
- **ChromaDB** - Vector database for semantic search
- **OpenAI** - Embeddings (text-embedding-3-small) + LLM (GPT-3.5/4)
- **LangChain** - LLM orchestration framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Docker** - Containerization

## 📊 How RAG Works

1. **Document Processing**
   - Upload PDF/DOCX/TXT
   - Extract text
   - Split into chunks (1000 chars, 200 overlap)

2. **Vectorization**
   - Convert chunks to embeddings using OpenAI
   - Store in ChromaDB with metadata

3. **Query**
   - User asks question
   - Vectorize question
   - Find top-K similar chunks (semantic search)

4. **Answer Generation**
   - Send relevant chunks + question to GPT
   - GPT generates answer using only provided context
   - Return answer with source citations

## 🧪 Testing

### Create test document
```bash
cat > test_doc.txt << 'EOF'
Employee Handbook

Section 1: Salary
Base salary: $80,000 per year
Payment: Bi-weekly

Section 2: Benefits
- Health insurance
- 15 days vacation
- 401k matching
EOF
```

### Upload and test
```bash
# Upload
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@test_doc.txt" \
  -F "title=Test Doc"

# Ask
curl -X POST "http://localhost:8000/api/v1/chat/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the salary?"}'
```

## 🚦 Development

### Project was built with

- Python 3.9+
- FastAPI best practices
- Clean architecture (separation of concerns)
- Type hints throughout
- Structured logging

### Key learnings

- RAG implementation from scratch
- Vector database integration
- LLM prompt engineering
- Production-ready FastAPI structure

## 📈 Future Enhancements

- [ ] Authentication & authorization
- [ ] Multi-user support
- [ ] Advanced RAG (re-ranking, hybrid search)
- [ ] Frontend UI (React/Vue)
- [ ] Caching layer
- [ ] Model fine-tuning
- [ ] Monitoring & analytics
- [ ] Deploy to cloud (AWS/GCP/Azure)

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Database connection error:**
```bash
docker-compose down -v
docker-compose up -d
```

**Module not found:**
```bash
python -m src.main  # Not: python src/main.py
```

## 📝 License

MIT

## 👨‍💻 Author

Built as a learning project for RAG implementation and production FastAPI development.

## 🙏 Acknowledgments

- OpenAI for embeddings and LLM
- LangChain for RAG framework
- FastAPI community

---

**⭐ Star this repo if you found it helpful!**
