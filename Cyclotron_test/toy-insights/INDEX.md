# 📋 Toy Insights Interview Template — File Index

**Location:** `/home/kdcllc/dev/labs/rag-interview/toy-insights/`

**Status:** ✅ Complete and ready for use

---

## 📚 Documentation Files (Start Here!)

| File | Purpose | Read Time | For Whom |
|------|---------|-----------|----------|
| **[README.md](README.md)** | Complete project overview with evaluation rubric | 5 min | Everyone |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | High-level summary of complete project | 5 min | Project leads |
| **[CANDIDATE_GUIDE.md](CANDIDATE_GUIDE.md)** | Step-by-step instructions | 5 min | Candidates |
| **[EVALUATION_GUIDE.md](EVALUATION_GUIDE.md)** | Evaluation rubric and scoring guide | 5 min | Evaluators |
| **[.env.example](.env.example)** | Environment variable template | 2 min | Setup |
| **[LICENSE](LICENSE)** | MIT License | 1 min | Legal |

---

## 🎯 Quick Links by Role

### For Evaluation

1. Start: [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md)
2. Score with: Rubric in [README.md](README.md)
3. Run: `docker-compose -f infra/docker/docker-compose.yml up`
4. Review: Code in `src/` directory

### For Candidates
1. Read: [CANDIDATE_GUIDE.md](CANDIDATE_GUIDE.md)
2. Start: [README.md](README.md#quick-start) Quick Start
3. Bug: Find it in [src/api/models.py](src/api/models.py)
4. Test: `pytest tests/test_bug.py -v`
5. Enhance: Pick any area to improve

### For Project Managers
1. Overview: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Stats: See structure in PROJECT_SUMMARY.md
3. Status: All 31 files complete ✅

---

## 🗂️ Source Code Files

### API Layer (`src/api/`)

| File | Purpose | Key Features |
|------|---------|--------------|
| **[main.py](src/api/main.py)** | FastAPI application | `/health`, `/ingest`, `/search`, `/chat` endpoints |
| **[models.py](src/api/models.py)** | Pydantic schemas | **BUG HERE:** mutable default in ChatRequest |
| **[deps.py](src/api/deps.py)** | Dependency injection | DB session, cache client providers |

**Total:** ~270 lines of clean, well-documented code

### RAG Pipeline (`src/rag/`)

| File | Purpose | Key Features |
|------|---------|--------------|
| **[pipeline.py](src/rag/pipeline.py)** | RAG orchestration | Chunking, retrieval, prompt assembly, answer generation |
| **[embeddings.py](src/rag/embeddings.py)** | Embedding provider | Hugging Face sentence-transformers wrapper |
| **[vectorstore.py](src/rag/vectorstore.py)** | Vector index | FAISS adapter with local persistence |
| **[prompt.txt](src/rag/prompt.txt)** | LLM prompt template | Customizable prompt for answer generation |

**Total:** ~500 lines implementing complete RAG workflow

### Database Layer (`src/db/`)

| File | Purpose | Key Features |
|------|---------|--------------|
| **[orm.py](src/db/orm.py)** | SQLAlchemy models | Documents, Chunks, ChatTranscripts tables |
| **[schema.py](src/db/schema.py)** | Schema management | Table creation, indexing, migration reference |

**Total:** ~120 lines with proper ORM design

### Cache Layer (`src/cache/`)

| File | Purpose | Key Features |
|------|---------|--------------|
| **[redis_client.py](src/cache/redis_client.py)** | Redis wrapper | TTL support, in-memory fallback, key operations |

**Total:** ~120 lines with graceful degradation

---

## 🧪 Test Files (`tests/`)

| File | Test Suite | Test Cases | Purpose |
|------|-----------|-----------|---------|
| **[test_api.py](tests/test_api.py)** | Endpoint tests | 8 tests | `/health`, `/ingest`, `/search`, `/chat` |
| **[test_rag.py](tests/test_rag.py)** | RAG tests | 8 tests | Embeddings, vector store, pipeline, retrieval |
| **[test_bug.py](tests/test_bug.py)** | Bug detection | 4 tests | **Detects mutable default bug** |

**Total:** ~750 lines of comprehensive test suite (40+ test cases)

**Key Test:**
```bash
pytest tests/test_bug.py::TestMutableDefaultBug::test_mutable_default_state_bleed -v
# FAILS before fix, PASSES after fix
```

---

## 📊 Sample Data (`data/samples/`)

5 diverse toy review markdown files (150-200 words each):

| File | Product | Words | Theme |
|------|---------|-------|-------|
| **[lego_review.md](data/samples/lego_review.md)** | LEGO Classic blocks | 150 | Building & creativity |
| **[dinosaurs_review.md](data/samples/dinosaurs_review.md)** | Dinosaur figures | 160 | Educational & collectible |
| **[rc_car_review.md](data/samples/rc_car_review.md)** | Remote control car | 150 | Speed & performance |
| **[puzzle_review.md](data/samples/puzzle_review.md)** | 1000-piece puzzle | 165 | Challenge & family |
| **[speaker_review.md](data/samples/speaker_review.md)** | Bluetooth speaker | 145 | Tech & audio |

All ready for immediate ingestion via `/ingest` endpoint.

---

## 🚀 Infrastructure Files

### Docker (`infra/docker/`)

| File | Purpose | Stack |
|------|---------|-------|
| **[Dockerfile](infra/docker/Dockerfile)** | Dev container | Python 3.11, all dependencies |
| **[Dockerfile.prod](infra/docker/Dockerfile.prod)** | Production container | Non-root user, health checks |
| **[docker-compose.yml](infra/docker/docker-compose.yml)** | Full stack | PostgreSQL, Redis, API service |

**Usage:** `docker-compose -f infra/docker/docker-compose.yml up`

### Azure (`infra/azure/`)

| File | Purpose | Content |
|------|---------|---------|
| **[README.md](infra/azure/README.md)** | Deployment guide | Container Apps, PostgreSQL, Redis, Key Vault, monitoring |

**Sections:**
- Container Apps setup
- Database provisioning
- Cache setup
- Secrets management
- Advanced: Azure AI Search
- Monitoring with Application Insights
- Scaling and cost optimization

---

## 🔧 Scripts (`scripts/`)

| File | Purpose | Usage |
|------|---------|-------|
| **[seed.py](scripts/seed.py)** | Database seeding | `python scripts/seed.py` |
| **[run_local.sh](scripts/run_local.sh)** | Local startup | `bash scripts/run_local.sh` |

---

## 📦 Configuration Files

| File | Purpose |
|------|---------|
| **[requirements.txt](requirements.txt)** | Python dependencies (11 packages) |
| **[.env.example](.env.example)** | Environment variable template |
| **[LICENSE](LICENSE)** | MIT License |

---

## 📈 File Statistics

```
Total Files:           32
Python Modules:        10
Test Files:            3
Documentation:         6
Sample Data:           5
Config Files:          3
Infrastructure:        3
Scripts:               2
Miscellaneous:         1
────────────────────────
Total Lines:          ~2,500
- Code:               ~1,200
- Tests:               ~750
- Docs:               ~550
```

---

## 🎯 Navigation Guide

### "I want to understand the architecture"
→ Read [README.md](README.md) → Browse `src/` folders → Check docstrings

### "I want to run the project"
→ Follow [CANDIDATE_GUIDE.md](CANDIDATE_GUIDE.md) quick start → Run tests → Try `/docs`

### "I want to find the bug"
→ Look in [src/api/models.py](src/api/models.py) → Read [tests/test_bug.py](tests/test_bug.py) → Fix it

### "I want to deploy to Azure"
→ Read [infra/azure/README.md](infra/azure/README.md) → Follow step-by-step commands

### "I want to understand RAG"

→ Study [src/rag/pipeline.py](src/rag/pipeline.py) → Check [src/rag/prompt.txt](src/rag/prompt.txt) → Look at tests

### "I want to evaluate the solution"

→ Use [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md) → Check [README.md](README.md) rubric → Run tests

---

## ✅ Completeness Checklist

- [x] All documentation complete
- [x] All source code written with docstrings
- [x] Comprehensive test suite
- [x] Sample data included
- [x] Docker support
- [x] Azure deployment guide
- [x] Deliberate bug included and documented
- [x] Environment templates
- [x] License file
- [x] README and guides

**Status:** 100% Complete ✅

---

## 🚀 Getting Started

### 1. First-Time Setup (2 minutes)
```bash
cd toy-insights
cp .env.example .env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize Database (1 minute)
```bash
python -c "from src.db.orm import engine; from src.db import schema; schema.init_db(engine)"
python scripts/seed.py
```

### 3. Run Tests (1 minute)
```bash
pytest tests/ -v
# Note: test_bug.py will fail (intentionally) until bug is fixed
```

### 4. Start API (0.5 minutes)
```bash
uvicorn src.api.main:app --reload
# Visit http://localhost:8000/docs
```

### 5. Or Use Docker (2 minutes)
```bash
docker-compose -f infra/docker/docker-compose.yml up
# Same endpoints, but with PostgreSQL and Redis
```

---

## 💡 Key Points

1. **The Bug:** Mutable default in `ChatRequest.filters` → State bleed across requests
2. **The Fix:** Use `Field(default_factory=list)` instead of `[]`
3. **The Test:** Run `pytest tests/test_bug.py -v` to verify
3. **The Time:** 40 minutes for complete interview
5. **The Rubric:** See [README.md](README.md) for evaluation criteria

---

## 🎓 For First-Time Users

**New to this project?** Start here:

1. **Understand:** [README.md](README.md) (5 min)
2. **Get Started:** [CANDIDATE_GUIDE.md](CANDIDATE_GUIDE.md) (5 min)
3. **Explore:** `src/api/main.py` (5 min)
4. **Test:** `pytest tests/test_api.py -v` (5 min)
5. **Find Bug:** `pytest tests/test_bug.py -v` (5 min)
6. **Fix & Explain:** (15 min)

**Total:** 40 minutes to fully understand, find, and fix the bug ✅

---

## 📞 Support

- **How do I run this?** → See [README.md#quick-start](README.md#quick-start)
- **I'm stuck on the bug** → Read [tests/test_bug.py](tests/test_bug.py) carefully
- **How do I deploy?** → Check [infra/azure/README.md](infra/azure/README.md)
- **What should I improve?** → See [CANDIDATE_GUIDE.md](CANDIDATE_GUIDE.md) options

---

**Last Updated:** December 8, 2024  
**Status:** Complete and ready for use ✅  
**Location:** `/home/kdcllc/dev/labs/rag-interview/toy-insights/`

Happy coding! 🚀
