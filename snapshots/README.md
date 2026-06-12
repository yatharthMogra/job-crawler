# Database snapshots

Pre-built PostgreSQL dumps let you skip job ingestion, LLM enrichment, and profile setup when running the stack locally.

## Quick start

1. Get a dump file (from a teammate or generate your own — see below).
2. Place it under `exports/` (gitignored).
3. Import:

```bash
./scripts/import-dev-db.sh exports/jobingestion-lite-YYYY-MM-DD.dump
```

4. Start services:

```bash
./scripts/dev-profile-service.sh
./scripts/dev-recommendation-service.sh
# job_ingestion optional — only needed for fetching new jobs
```

5. Open the web app with a known candidate id from `exports/manifest-*.json`:

```
http://localhost:3000/jobs/recommended?candidate_id=<UUID>
```

## Dump variants

| File | Contents |
|------|----------|
| `jobingestion-full-*.dump` | Complete database including `raw_jobs`, pipeline runs, enrichment audit tables |
| `jobingestion-lite-*.dump` | Data-only for jobs index + profiles + subscriptions (schema created by Alembic on import) |

Lite data includes `companies`, `raw_jobs`, `normalized_jobs`, profile tables, `user_pool_subscriptions`, and alembic version rows. Operational tables (pipeline runs, enrichment queue, notification history) start empty.

## Generate a new export

```bash
./scripts/export-dev-db.sh
```

Writes to `exports/`:

- `jobingestion-full-YYYY-MM-DD.dump`
- `jobingestion-lite-YYYY-MM-DD.dump`
- `manifest-YYYY-MM-DD.json` (row counts, alembic heads, recommended candidate UUIDs, checksums)

## Requirements

- Docker (Postgres via `job_ingestion/docker-compose.yml`)
- Repo venv for lite imports (`./scripts/setup-env.sh`) — migrations recreate operational tables excluded from the lite dump

Import **drops and recreates** the `jobingestion` database.

## Notes

- All three services share one database: `jobingestion`.
- Resume PDF files are **not** in the dump; only DB rows. Pre-built profiles work without PDFs.
- Dumps may contain real user emails — share privately, not in git (`exports/` is gitignored).
