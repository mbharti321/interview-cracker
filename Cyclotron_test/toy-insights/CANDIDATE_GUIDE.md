# Candidate Getting Started Guide

## Welcome to Toy Insights! 👋

This is an interview template project that tests your ability to work with:
- **Python backend** (FastAPI, SQLAlchemy)
- **Machine Learning** (embeddings, vector search, RAG)
- **Database design** (PostgreSQL, schema design)
- **Caching** (Redis with TTL)
- **Cloud deployment** (Azure awareness)
- **Testing & debugging** (identifying and fixing bugs)

---

## Step 1: Understand the Project (5 minutes)

### What does this app do?
1. Reads toy product reviews from markdown files
2. Splits them into chunks and creates vector embeddings
3. Stores metadata in a PostgreSQL database
4. Allows users to search via `/search` endpoint or ask questions via `/chat`
5. Uses RAG (Retrieval-Augmented Generation) to answer questions with sources
6. Caches answers in Redis for performance

### Key concepts
- **RAG:** Retrieve relevant documents → Augment prompt with context → Generate answer
- **Embeddings:** Convert text to numerical vectors for similarity search
- **Vector Store:** Index for fast nearest-neighbor search (using FAISS)
- **Caching:** Store recent answers with TTL to avoid redundant work

---

## Step 2: Explore the Code (5 minutes)

### Start here:
1. **[README.md](README.md)** - Project overview and evaluation rubric
2. **[src/api/main.py](src/api/main.py)** - FastAPI endpoints
3. **[src/api/models.py](src/api/models.py)** - Request/response schemas
4. **[src/rag/pipeline.py](src/rag/pipeline.py)** - RAG orchestration

### Run the tests to understand expected behavior:
```bash
pytest tests/ -v
```

Most tests should pass. Notice that `tests/test_bug.py` **will fail** — that's intentional.

---

## Step 3: Find and Fix the Bug (20 minutes)

### The Challenge
There's a **deliberate bug** in the starter code. Your job is to:
1. Identify the bug
2. Write a test that fails because of it
3. Fix the bug
4. Verify the test passes

### Where's the bug?
Look in `src/api/models.py` → `ChatRequest` class

**Hint:** It's a common Python gotcha related to mutable defaults.

### How to detect it
```bash
pytest tests/test_bug.py::TestMutableDefaultBug::test_mutable_default_state_bleed -v
```

This test currently FAILS. After you fix it, it should PASS.

### How to understand it
Read the detailed explanation in [`tests/test_bug.py`](tests/test_bug.py).

### How to fix it
The fix is simple (1-2 lines):
- Change the mutable default to use `Field(default_factory=list)`
- Verify all tests pass

---

## Step 4: Explain Your Work (10 minutes)

Discuss what you've accomplished:

- **The bug:** What was it? How did you identify it?
- **The fix:** What changes did you make? Why were they correct?
- **Testing:** How did you verify the fix worked?
- **Understanding:** Explain key concepts from the codebase

---

## Testing During the Interview

```bash
# Run all tests to verify the fix
pytest tests/ -v

# The test that detects the bug
pytest tests/test_bug.py::TestMutableDefaultBug -v
```

---

## FAQ & Troubleshooting

### "I don't have PostgreSQL installed"
No problem! The code falls back to SQLite (see `.env.example`):
```
DATABASE_URL=sqlite:///./toy_insights.db
```

### "Redis not running"
Also fine! The code falls back to in-memory cache (see `src/cache/redis_client.py`).

### "Embedding model download is slow"
First run downloads the model (~100MB). It's cached locally.
Or use mock embeddings (already implemented as fallback).

### "Tests are failing"
1. Check imports: `pip install -r requirements.txt`
2. Verify `.env` is set up: `cp .env.example .env`
3. Initialize DB: `python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"`
4. Seed data: `python scripts/seed.py`

### "I broke something"
1. Check git status: `git status`
2. Revert a file: `git checkout src/api/main.py`
3. Reset everything: `git reset --hard`

---

## Evaluation Rubric (for reference)

Your work will be evaluated on:

| Metric | %   | What we're looking for |
|--------|-----|---|
| Architecture & Code Quality | 20% | Clear structure, good naming, proper error handling |
| API Correctness | 20% | Endpoints work as specified, validation with Pydantic |
| RAG Quality | 20% | Good retrieval, sensible answers, proper citations |
| Data & Cache | 15% | DB works, caching reduces work, queries are efficient |
| Testing | 15% | Tests pass, good coverage, bug is identified & fixed |
| Azure Awareness | 10% | Can explain Container Apps, Key Vault, deployment flow |

---

## Time Allocation (Suggested)

- **Understand:** 5 min
- **Explore & Find Bug:** 10 min
- **Fix Bug:** 15 min
- **Verify & Explain:** 10 min

**Total: 40 minutes**

---

## Key Files to Study

1. **[src/api/main.py](src/api/main.py)** - Start here for API structure
2. **[src/api/models.py](src/api/models.py)** - The bug is here!
3. **[src/rag/pipeline.py](src/rag/pipeline.py)** - RAG orchestration
4. **[tests/test_bug.py](tests/test_bug.py)** - Understanding the bug
5. **[README.md](README.md)** - Full context & evaluation rubric

---

## Quick Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Initialize
python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"
python scripts/seed.py

# Run
uvicorn src.api.main:app --reload

# Test
pytest tests/ -v
pytest tests/test_bug.py -v  # The failing test

# Docker
docker-compose -f infra/docker/docker-compose.yml up
```

---

## Need Help?

1. **Read the docstrings** — Most functions explain themselves
2. **Look at existing tests** — Show expected behavior
3. **Check error messages** — Usually tell you exactly what's wrong
4. **Ask clarifying questions** — Thoughtful questions demonstrate engagement

---

Good luck! You've got this! 🚀
