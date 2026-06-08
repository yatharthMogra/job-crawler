# Profile Service

Standalone FastAPI backend for candidate profile intelligence: resume ingestion, LLM evidence extraction, user-approved patches, versioned profiles, and derived capabilities.

Shares the PostgreSQL instance with `job_ingestion` but uses separate tables and runs on port **8001**.

**Requires Python 3.11+.** Use the shared repo-root virtualenv (see [testing.md](testing.md) and [../README.md](../README.md)).

Quick start:

```bash
# from repo root
./scripts/dev-profile-service.sh
# or: ./profile_service/scripts/dev.sh
```

See [testing.md](testing.md) for setup and curl examples.
