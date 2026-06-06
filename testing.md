```bash
# Set base URL once
BASE="http://127.0.0.1:8000"
```

```bash
# 1) GET /companies
curl -sS "$BASE/companies" | jq
```

```bash
# 2) POST /pipeline/trigger
curl -sS -X POST "$BASE/pipeline/trigger" | jq
```

```bash
# 3a) GET /pipeline/runs
curl -sS "$BASE/pipeline/runs" | jq
```

```bash
# 3b) GET /pipeline/runs/{run_id}
# replace <RUN_ID> from previous response
curl -sS "$BASE/pipeline/runs/<RUN_ID>" | jq
```

```bash
# 4) GET /jobs?limit=20
curl -sS "$BASE/jobs?limit=20" | jq
```

```bash
# 5a) GET /jobs/{job_id}
# replace <JOB_ID> from previous response
curl -sS "$BASE/jobs/<JOB_ID>" | jq
```

```bash
# 5b) GET /jobs/{job_id}/raw
curl -sS "$BASE/jobs/<JOB_ID>/raw" | jq
```

```bash
# 6a) GET /events?limit=50
curl -sS "$BASE/events?limit=50" | jq
```

```bash
# 6b) GET /events/summary
curl -sS "$BASE/events/summary" | jq
```

Optional quick automation for IDs:

```bash
RUN_ID=$(curl -sS "$BASE/pipeline/runs" | jq -r '.[0].id')
JOB_ID=$(curl -sS "$BASE/jobs?limit=20" | jq -r '.[0].id')

curl -sS "$BASE/pipeline/runs/$RUN_ID" | jq
curl -sS "$BASE/jobs/$JOB_ID" | jq
curl -sS "$BASE/jobs/$JOB_ID/raw" | jq
```

If your API is not on localhost, change `BASE` once and all commands still work.