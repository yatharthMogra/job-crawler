# Embedding Worker — Isolating ONNX/ML Deps from `profile_service`

**Goal:** keep `profile_service` slim and fast (no PyTorch/ONNX in its image), compute embeddings
in a separate, purpose-built Cloud Run component, near-real-time on upload and via a scheduled
catch-up job — no dependency on personal hardware.

---

## 1. Architecture at a glance

```
Resume upload / job ingestion
        │
        ▼
profile_service (Cloud Run service — unchanged deps, no ML)
        │  publish {entity_type, entity_id} to Pub/Sub
        ▼
Pub/Sub topic: "embedding-requests"
        │  push subscription
        ▼
embedding-worker (new Cloud Run service — the ONLY place ONNX/onnxruntime/model live)
        │  compute embedding, write to DB
        ▼
Supabase (content_embedding column populated)

                    ┌── separate path, same image ──┐
Cloud Scheduler ──▶ Cloud Run JOB (embedding-backfill)  ── catches anything missed:
                    failed messages, DLQ overflow, initial migration backfill
```

Two invocation shapes, one shared Docker image:
- **`embedding-worker`** (Cloud Run *service*): Pub/Sub push-triggered, handles the hot path —
near-real-time, one message per resume/job.
- **`embedding-backfill`** (Cloud Run *Job*, via Cloud Scheduler, e.g. nightly): batch mode, queries
`WHERE content_embedding IS NULL`, catches anything the push path missed. This replaces the "run a
cron on your home machine" idea entirely — same logic, same image, runs in GCP, monitored the same
way as everything else.

---

## 2. `profile_service` changes (the slim side)

No new dependencies. On resume upload / job ingestion, instead of calling `embed_text()` inline,
publish a small message:

```python
# profile_service — after resume saved
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, "embedding-requests")

publisher.publish(
    topic_path,
    json.dumps({"entity_type": "resume", "entity_id": resume_id}).encode("utf-8"),
)
```

This call is fire-and-forget from `profile_service`'s perspective — publishing to Pub/Sub is
milliseconds, doesn't block the upload response, and doesn't require `profile_service` to know
anything about embeddings, ONNX, or models at all. If this publish call fails, the resume upload
should still succeed (same "fail gracefully" behavior your agent already built for the inline
`embed_text()` case) — log it, and rely on the nightly backfill job to catch it since it queries by
`content_embedding IS NULL`, not by "did a message get published."

---

## 3. `embedding-worker` (the ONNX side)

### 3.1 Dockerfile — bake the model in at build time, per the earlier fix

```dockerfile
FROM python:3.11-slim

# onnxruntime, not torch/sentence-transformers — much smaller install
RUN pip install --no-cache-dir onnxruntime tokenizers huggingface-hub

# Download once, at build time — pin a revision so this is reproducible
RUN python -c "\
from huggingface_hub import snapshot_download; \
snapshot_download( \
    repo_id='sentence-transformers/all-MiniLM-L6-v2', \
    revision='<pin-a-specific-commit-hash>', \
    allow_patterns=['onnx/*', 'tokenizer*', 'vocab.txt', 'config.json'] \
)"

COPY worker/ /app/worker/
WORKDIR /app

# HF_HUB_OFFLINE=1 at RUNTIME (not build time) — tripwire against accidental network calls later
ENV HF_HUB_OFFLINE=1

CMD ["python", "worker/main.py"]
```

### 3.2 Handler (push subscription → HTTP endpoint)

Pub/Sub push subscriptions deliver messages as an HTTP POST to a Cloud Run service. Sketch:

```python
# worker/main.py
from fastapi import FastAPI, Request
import base64, json

app = FastAPI()
model = load_onnx_model()  # loaded once per container instance, not per request

@app.post("/")
async def handle_push(request: Request):
    envelope = await request.json()
    message = envelope["message"]
    payload = json.loads(base64.b64decode(message["data"]))

    entity_type, entity_id = payload["entity_type"], payload["entity_id"]
    text = fetch_text(entity_type, entity_id)          # resume text or job description
    vector = model.embed(text)                          # ONNX inference, tens of ms
    write_embedding(entity_type, entity_id, vector)      # write back to Supabase

    return {"status": "ok"}, 200   # 2xx acks the message; non-2xx triggers Pub/Sub retry
```

Returning a non-2xx (or timing out) causes Pub/Sub to retry with backoff automatically — no custom
retry logic needed in the handler itself.

### 3.3 Dead-letter handling

Configure a dead-letter topic on the subscription (a few lines of Pub/Sub config, not application
code) so messages that fail repeatedly (e.g. malformed payload, entity deleted before the message
was processed) land somewhere inspectable instead of retrying forever or silently vanishing. The
nightly backfill job is the practical safety net underneath this — even if a message is
dead-lettered and nobody notices immediately, the next backfill run picks up that resume anyway
since it queries by missing-embedding state, not by message status.

---

## 4. `embedding-backfill` (Cloud Run Job, scheduled)

Same Docker image as the worker, different entrypoint — reuses the exact same ONNX loading code,
just runs in batch mode instead of handling one push request:

```python
# worker/backfill.py — run via `gcloud run jobs execute`
def run_backfill():
    rows = query("SELECT id, type, text FROM ... WHERE content_embedding IS NULL LIMIT 500")
    for row in rows:
        vector = model.embed(row.text)
        write_embedding(row.type, row.id, vector)
```

This is the fix your agent flagged was missing in the existing script — filtering by
`content_embedding IS NULL` rather than "always re-embed the latest 500" — now it's a proper
catch-up job, not a redundant re-computation.

Scheduled via Cloud Scheduler hitting the Cloud Run Jobs API on a cron (nightly is a reasonable
default, given the push path should catch the vast majority of cases in near-real-time):

```bash
gcloud scheduler jobs create http embedding-backfill-nightly \
  --schedule="0 3 * * *" \
  --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/<project>/jobs/embedding-backfill:run" \
  --http-method=POST \
  --oauth-service-account-email=<scheduler-sa>@<project>.iam.gserviceaccount.com
```

---

## 5. GCP resources to provision

```bash
# Topic
gcloud pubsub topics create embedding-requests --project job-crawler-243-55

# Dead-letter topic
gcloud pubsub topics create embedding-requests-dlq --project job-crawler-243-55

# Push subscription → embedding-worker service
gcloud pubsub subscriptions create embedding-requests-sub \
  --topic=embedding-requests \
  --push-endpoint=https://embedding-worker-<hash>-uc.a.run.app/ \
  --push-auth-service-account=<invoker-sa>@job-crawler-243-55.iam.gserviceaccount.com \
  --dead-letter-topic=embedding-requests-dlq \
  --max-delivery-attempts=5

# embedding-worker service (deploy from the Dockerfile above)
gcloud run deploy embedding-worker \
  --image=us-central1-docker.pkg.dev/job-crawler-243-55/<repo>/embedding-worker:latest \
  --region=us-central1 \
  --no-allow-unauthenticated \
  --memory=512Mi

# embedding-backfill job (same image, different entrypoint/command override)
gcloud run jobs create embedding-backfill \
  --image=us-central1-docker.pkg.dev/job-crawler-243-55/<repo>/embedding-worker:latest \
  --region=us-central1 \
  --command="python" --args="worker/backfill.py" \
  --memory=512Mi
```

`--no-allow-unauthenticated` + `--push-auth-service-account` ensures only Pub/Sub (with the right
service account) can hit the worker's endpoint — not open to the public internet.

---

## 6. Cost, concretely

- **`embedding-worker`**: billed only while handling a push request (Cloud Run's standard
per-request/per-second billing) — for a niche job board's upload volume, this is a small number of
brief invocations per day, likely within or close to Cloud Run's free tier.
- **`embedding-backfill`**: Cloud Run Jobs bill only for actual execution time, once a night — a
batch of up to 500 ONNX embeddings at tens-of-ms each is seconds of runtime, not minutes.
- **Pub/Sub**: priced per message and per GB; at this volume (one message per resume save / job
ingestion) this is fractions of a cent.
- **Net effect vs. today**: you're not adding a meaningfully billable component — you're moving the
existing (currently-failing) embedding computation into a properly isolated, monitored place, and
the compute cost of that work was already established as trivial in the earlier ATS-score costing.

---

## 7. Migration steps

1. Add `HF_TOKEN` to the `embedding-worker` build/deploy (Secret Manager, per the earlier
recommendation) — needed once at image-build time to download the model, not at runtime given
`HF_HUB_OFFLINE=1`.
2. Build and deploy `embedding-worker` and `embedding-backfill` (Section 5).
3. Add the Pub/Sub publish call to `profile_service` (Section 2) — this can ship before the worker
even exists; messages just queue until a subscription is listening.
4. Wire up the subscription once the worker is live.
5. Run `embedding-backfill` once manually (`gcloud run jobs execute embedding-backfill`) to catch
up anything created before this pipeline existed, then let the nightly schedule take over.
6. Confirm the root `profile_service` Dockerfile never installs `onnxruntime`/`torch` — that
dependency should exist in exactly one image, the worker's.

---

## 8. Open items

1. **Memory allocation for `embedding-worker`** — 512Mi in the sketch above is a reasonable starting
guess for ONNX Runtime + a 22M-parameter model; worth confirming empirically once deployed rather
than trusting the estimate.
2. **`fetch_text()` / `write_embedding()`** in the handler sketch are stand-ins for your actual
Supabase read/write calls — not fleshed out here since they're just existing DB access patterns,
not new architecture.
3. **Auth between `profile_service` and Pub/Sub** — needs a service account with `pubsub.publisher`
on the topic; not detailed here, standard IAM grant.
