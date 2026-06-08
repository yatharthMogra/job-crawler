# Profile Service — Manual Test Recipes

Start Postgres (shared with job ingestion):

```bash
cd ../job_ingestion && docker compose up -d postgres
```

Install and migrate (uses the **repo-root** virtualenv — see [`../README.md`](../README.md)):

```bash
cd ..   # repo root
./scripts/setup-env.sh
source job-crawler/bin/activate
cd profile_service
cp .env.example .env
alembic upgrade head
```

Note: profile service uses a separate Alembic version table (`alembic_version_profile`) so it can share the `jobingestion` database with job_ingestion without migration conflicts.

Run the service:

```bash
# from repo root
./scripts/dev-profile-service.sh
```

Or from `profile_service/` after activating the root venv:

```bash
source ../job-crawler/bin/activate
uvicorn app.main:app --port 8001 --reload
```

Do **not** run `uvicorn` from a global/conda Python 3.9 environment. The codebase requires Python 3.11+.

Seed test data:

```bash
python -m app.utils.seed
```

## API Examples

Set variables:

```bash
export API_KEY=dev-key-change-me
export BASE=http://localhost:8001
```

Health (no auth):

```bash
curl "$BASE/health"
```

Create candidate:

```bash
curl -X POST "$BASE/candidates" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"Your Name"}'
```

Upload resume (replace CANDIDATE_ID and path):

```bash
curl -X POST "$BASE/candidates/CANDIDATE_ID/resumes/upload" \
  -H "X-API-Key: $API_KEY" \
  -F "file=@/path/to/resume.pdf"
```

Get pending patch:

```bash
curl "$BASE/candidates/CANDIDATE_ID/patches/pending" -H "X-API-Key: $API_KEY"
```

Commit patch (replace PATCH_ID and operation IDs from pending response):

```bash
curl -X POST "$BASE/candidates/CANDIDATE_ID/patches/PATCH_ID/commit" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"approved_operation_ids":["OP_ID_1","OP_ID_2"]}'
```

Get profile and capabilities:

```bash
curl "$BASE/candidates/CANDIDATE_ID/profile" -H "X-API-Key: $API_KEY"
curl "$BASE/candidates/CANDIDATE_ID/capabilities" -H "X-API-Key: $API_KEY"
```

Direct education edit:

```bash
curl -X PATCH "$BASE/candidates/CANDIDATE_ID/profile/education" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"degree":"MS Computer Science","university":"NYU","graduation_date":"2027-05"}'
```
