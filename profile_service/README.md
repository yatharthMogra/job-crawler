# Profile Service

Standalone FastAPI backend for candidate profile intelligence: resume ingestion, LLM evidence extraction, user-approved patches, versioned profiles, and derived capabilities.

Shares the PostgreSQL instance with `job_ingestion` but uses separate tables and runs on port **8001**.

**Requires Python 3.11+.** Use the project virtualenv (see [testing.md](testing.md)).

Quick start:

```bash
source .venv/bin/activate
uvicorn app.main:app --port 8001 --reload
# or: ./scripts/dev.sh
```

See [testing.md](testing.md) for setup and curl examples.
