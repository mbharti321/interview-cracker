# Toy Insights RAG Service

A hands-on interview template project that implements a **Retrieval-Augmented Generation (RAG)** service for toy product reviews and insights.

## 🎯 Project Overview

**Toy Insights** is a lightweight FastAPI service that:
1. **Ingests** toy product reviews and descriptions from markdown files
2. **Builds** a local vector index (FAISS) for semantic search
3. **Retrieves** relevant context using embeddings
4. **Generates** RAG-based answers with source citations
5. **Caches** frequent queries in Redis to improve performance
6. **Persists** chat transcripts and metadata in PostgreSQL

**Target Time:** 40 minutes for candidates to complete

**Difficulty:** Intermediate (suitable for senior mid-level engineers)

---

## 📋 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional, for full stack)
- Git

### Local Setup (without Docker)

```bash
# 1. Clone and navigate
cd toy-insights

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Run database migrations
python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"

# 6. Seed sample data
python scripts/seed.py

# 7. Start API server
uvicorn src.api.main:app --reload --port 8000
```

**API available at:** `http://localhost:8000`

**Interactive docs:** `http://localhost:8000/docs`

### Full Stack with Docker

```bash
# Start all services (PostgreSQL, Redis, API)
bash scripts/run_local.sh

# Check services
docker-compose -f infra/docker/docker-compose.yml ps

# View logs
docker-compose -f infra/docker/docker-compose.yml logs -f api

# Stop services
docker-compose -f infra/docker/docker-compose.yml down
```

---

## 🏗️ Project Structure

```
toy-insights/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # Route handlers & app setup
│   │   ├── models.py           # Pydantic request/response schemas [BUG HERE]
│   │   └── deps.py             # Dependency injection
│   ├── rag/                    # RAG pipeline
│   │   ├── embeddings.py       # Text-to-vector conversion
│   │   ├── vectorstore.py      # FAISS index management
│   │   ├── pipeline.py         # RAG orchestration
│   │   └── prompt.txt          # LLM prompt template
│   ├── db/                     # Database layer
│   │   ├── orm.py              # SQLAlchemy models
│   │   └── schema.py           # Schema initialization
│   └── cache/
│       └── redis_client.py     # Redis wrapper with TTL
├── data/
│   └── samples/                # Sample markdown documents
├── tests/
│   ├── test_api.py             # Endpoint tests
│   ├── test_rag.py             # RAG component tests
│   └── test_bug.py             # Deliberate bug detection test
├── infra/
│   ├── docker/                 # Docker & Compose config
│   └── azure/                  # Azure deployment guide
├── scripts/
│   ├── seed.py                 # Database seeding script
│   └── run_local.sh            # Local startup helper
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🔌 API Endpoints

All endpoints are available with interactive documentation at `/docs` (Swagger UI).

### Health Check
```bash
GET /health
# Response: {"status": "ok"}
```

### Ingest Documents
```bash
POST /ingest
Content-Type: application/json

{
  "file_paths": [
    "data/samples/lego_review.md",
    "data/samples/dinosaurs_review.md"
  ]
}

# Response:
{
  "document_count": 2,
  "chunk_count": 15,
  "status": "success"
}
```

### Vector Store Search
```bash
GET /search?q=lego%20toy&k=5

# Response:
{
  "query": "lego toy",
  "results": [
    {
      "score": 0.92,
      "content": "LEGO Classic set with 300 bricks...",
      "document_id": 1,
      "source": "data/samples/lego_review.md"
    }
  ]
}
```

### RAG Chat (with caching)
```bash
POST /chat
Content-Type: application/json

{
  "query": "What toy would you recommend for a 5-year-old?",
  "k": 5,
  "filters": []
}

# Response:
{
  "answer": "Based on the toy reviews, I would recommend LEGO...",
  "sources": [
    {
      "document_id": 1,
      "source": "data/samples/lego_review.md",
      "score": 0.89,
      "snippet": "LEGO Classic building blocks..."
    }
  ],
  "cached": false
}
```

> **Note:** Second request with same query returns `cached: true`

---

## 🐛 The Deliberate Bug

### What is it?
**Mutable default in Pydantic model** causing cross-request state bleed.

### Location
`src/api/models.py` — `ChatRequest` class

### The Bug
```python
class ChatRequest(BaseModel):
    query: str
    k: int = 5
    filters: list[str] = []  # <-- BUG: mutable default!
```

### Why is it a bug?
Pydantic models cache mutable defaults. All instances share the same list object:
```python
req1 = ChatRequest(query="q1")
req2 = ChatRequest(query="q2")

req1.filters.append("filter1")
# req2.filters now also contains "filter1"! ❌
```

### The Fix
```python
from pydantic import Field

class ChatRequest(BaseModel):
    query: str
    k: int = 5
    filters: list[str] = Field(default_factory=list)  # ✅ Fixed!
```

### Detecting the Bug
```bash
# Run the test that detects the bug (currently fails)
pytest tests/test_bug.py::TestMutableDefaultBug::test_mutable_default_state_bleed -v

# After implementing the fix, it should pass
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Suite
```bash
# API endpoint tests
pytest tests/test_api.py -v

# RAG pipeline tests
pytest tests/test_rag.py -v

# Bug detection (should FAIL before fix, PASS after)
pytest tests/test_bug.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 📊 Evaluation Rubric

Use this rubric to assess the work:

| Category | Weight | Criteria |
|----------|--------|----------|
| **Architecture & Repo Hygiene** | 20% | Clear module boundaries (api/rag/db/cache), proper imports, docstrings, sensible file organization, useful README |
| **API Correctness** | 20% | Endpoints behave as specified, proper HTTP status codes, input validation with Pydantic, error handling |
| **RAG Quality** | 20% | Sensible chunking strategy, good retrieval relevance, prompt assembly with source citations, answer generation |
| **Data & Cache** | 15% | Database writes verified, Redis cache working (TTL respected), cache keys normalized, efficient queries |
| **Testing** | 15% | Unit/integration tests pass, test coverage > 70%, failing test identifies the bug, fix makes test pass |
| **Azure Awareness** | 10% | Candidate can explain deployment to Container Apps, Key Vault for secrets (even if not fully deployed) |

### Scoring Guide
- **90-100:** Exceptional. All requirements met, code is clean, demonstrates deep understanding.
- **80-89:** Good. Mostly correct, minor issues, good understanding of concepts.
- **70-79:** Acceptable. Core features work, some incomplete parts, basic understanding.
- **60-69:** Needs Work. Several issues, incomplete features, limited understanding.
- **<60:** Not Recommended. Major gaps, non-functional code, misses core concepts.

---

## 🔍 Component Details

### Embeddings (`src/rag/embeddings.py`)
- Uses Hugging Face `sentence-transformers` for semantic embeddings
- Falls back to mock embeddings (deterministic hash-based) if package unavailable
- Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dim embeddings)

### Vector Store (`src/rag/vectorstore.py`)
- FAISS (Facebook AI Similarity Search) for local vector indexing
- Persists index to `data/vectors/` directory
- Falls back to in-memory search if FAISS unavailable
- Supports efficient similarity search with L2 distance metric

### RAG Pipeline (`src/rag/pipeline.py`)
- **Chunking:** Splits documents into 300-char chunks with 50-char overlap
- **Retrieval:** Embeds query, searches for top-k similar chunks
- **Augmentation:** Constructs prompt with context from retrieved chunks
- **Generation:** Mock LLM (can replace with OpenAI, HuggingFace, etc.)
- **Caching:** 5-minute TTL on Redis for recent queries

### Database (`src/db/`)
- **ORM:** SQLAlchemy for model definitions
- **Tables:**
  - `documents`: Metadata for ingested files
  - `chunks`: Document chunks with indices
  - `chat_transcripts`: Chat history with sources
- **Connection:** PostgreSQL (or SQLite for local dev)

### Cache (`src/cache/redis_client.py`)
- Simple Redis wrapper with TTL support
- Falls back to in-memory mock if Redis unavailable
- Default TTL: 300 seconds (5 minutes)
- Used for `/chat` endpoint caching

---

## 🌐 Azure Deployment

See [`infra/azure/README.md`](infra/azure/README.md) for complete deployment guide.

### Quick Summary
1. **Azure Container Registry** → Store Docker image
2. **Azure Container Apps** → Run containerized service
3. **Azure Database for PostgreSQL** → Managed database
4. **Azure Cache for Redis** → Managed cache
5. **Azure Key Vault** → Secrets management
6. **Application Insights** → Monitoring & logging

### Deployment Command
```bash
bash infra/azure/deploy.sh  # (after implementing helper script)
```

---

## 📦 Dependencies

See `requirements.txt` for full list. Key packages:

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.4.2
sentence-transformers==2.2.2
faiss-cpu==1.7.4
redis==5.0.1
psycopg2-binary==2.9.9
pytest==7.4.3
```

### Optional (for full features)
- `openai` — For ChatGPT-based answer generation
- `langchain` — For advanced RAG patterns
- `azure-keyvault-secrets` — For Azure Key Vault integration
- `azure-search-documents` — For Azure AI Search integration

---

## 🚀 Performance Notes

- **Embedding:** ~50ms per document (CPU-based)
- **Vector Search:** <5ms for top-10 similarity search in 100-doc corpus
- **Cache Hit:** <1ms (Redis)
- **Cache Miss:** ~100-200ms (full RAG pipeline)

Optimize with:
- GPU embedding (CUDA-enabled transformers)
- Larger FAISS index (`IndexIVFFlat` for 100k+ docs)
- Batch ingestion (vectorize multiple docs in parallel)

---

## 🔒 Security Considerations

1. **Secrets:** Use `.env` file (never commit) or Azure Key Vault
2. **Database:** Use strong passwords, enable SSL for PostgreSQL
3. **Redis:** Configure password, bind to private network
4. **API:** Add authentication (JWT, OAuth2) before production
5. **Input Validation:** Pydantic models validate all inputs
6. **CORS:** Configure allowed origins if exposing to web

---

## 📝 Interview Tips for Candidates

### Time Management (40 min)
- **0-5 min:** Understand the codebase structure
- **5-15 min:** Run tests and locate the deliberate bug
- **15-35 min:** Fix the bug and verify tests pass
- **35-40 min:** Explain your work and discuss improvements

### Key Areas to Demonstrate
1. **Code Understanding:** Explain how each module works
2. **Problem Solving:** Fix the bug without breaking tests
3. **Testing:** Write/run tests to verify your changes
4. **Communication:** Explain your choices and trade-offs
5. **Iteration:** Show willingness to refactor and improve

### Common Improvements
- Add request logging and error tracking
- Implement document chunking strategies (recursive, sliding window)
- Add query expansion or synonym handling
- Integrate a real LLM (OpenAI, local LLaMA)
- Add batch ingestion endpoint
- Implement user authentication
- Add Azure deployment script

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [FAISS Tutorial](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [Sentence Transformers](https://www.sbert.net/)
- [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/)
- [RAG Patterns](https://python.langchain.com/docs/use_cases/question_answering/)

---

## 💡 Support & Questions

If stuck:
1. **Check existing code:** Similar patterns are used elsewhere
2. **Read docstrings:** Most functions have usage examples
3. **Run tests:** `pytest -v` shows expected behavior
4. **Read error messages:** Often indicate the exact problem
5. **Ask clarifying questions:** Thoughtful questions demonstrate engagement

---

## 📄 License

MIT License — See [`LICENSE`](LICENSE) file

---

## 🎓 Credits

Created as an interview template for evaluating software engineers on:
- Python backend development (FastAPI)
- Machine learning / RAG concepts
- Database design & querying
- Caching strategies
- Cloud deployment (Azure)
- Testing & debugging
- Code quality & documentation

**Good luck! 🚀**
