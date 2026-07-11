#!/usr/bin/env bash
# One-time GCP provisioning for the resume embedding worker pipeline.
#
# Creates Pub/Sub topics, push subscription, IAM grants, and nightly backfill scheduler.
# Run AFTER the first embedding-worker Cloud Run deploy (needs the service URL).
#
# Usage:
#   GCP_PROJECT=your-project-id GCP_REGION=us-central1 ./scripts/provision-embedding-infra.sh
#
# Optional overrides:
#   PUBSUB_PUSH_SA=embedding-pubsub-push@PROJECT.iam.gserviceaccount.com
#   SCHEDULER_SA=embedding-scheduler@PROJECT.iam.gserviceaccount.com
#
set -euo pipefail

PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
TOPIC="${EMBEDDING_REQUESTS_TOPIC:-embedding-requests}"
DLQ_TOPIC="${EMBEDDING_REQUESTS_DLQ_TOPIC:-embedding-requests-dlq}"
SUBSCRIPTION="${EMBEDDING_REQUESTS_SUBSCRIPTION:-embedding-requests-sub}"
PUSH_SA="${PUBSUB_PUSH_SA:-embedding-pubsub-push@${PROJECT}.iam.gserviceaccount.com}"
SCHEDULER_SA="${SCHEDULER_SA:-embedding-scheduler@${PROJECT}.iam.gserviceaccount.com}"

echo "==> Enabling APIs"
gcloud services enable pubsub.googleapis.com cloudscheduler.googleapis.com run.googleapis.com \
  --project "${PROJECT}"

WORKER_URL="$(gcloud run services describe embedding-worker \
  --project "${PROJECT}" \
  --region "${REGION}" \
  --format='value(status.url)')"
if [[ -z "${WORKER_URL}" ]]; then
  echo "ERROR: embedding-worker service not found. Deploy it first."
  exit 1
fi

echo "==> Creating Pub/Sub topics (if missing)"
gcloud pubsub topics create "${TOPIC}" --project "${PROJECT}" 2>/dev/null || true
gcloud pubsub topics create "${DLQ_TOPIC}" --project "${PROJECT}" 2>/dev/null || true

echo "==> Creating push service account (if missing)"
gcloud iam service-accounts create embedding-pubsub-push \
  --project "${PROJECT}" \
  --display-name="Pub/Sub push invoker for embedding-worker" 2>/dev/null || true

gcloud iam service-accounts create embedding-scheduler \
  --project "${PROJECT}" \
  --display-name="Cloud Scheduler invoker for embedding-backfill" 2>/dev/null || true

echo "==> Granting run.invoker on embedding-worker to push SA"
gcloud run services add-iam-policy-binding embedding-worker \
  --project "${PROJECT}" \
  --region "${REGION}" \
  --member="serviceAccount:${PUSH_SA}" \
  --role="roles/run.invoker"

echo "==> Granting pubsub.publisher on ${TOPIC} to profile-service default SA"
PROJECT_NUMBER="$(gcloud projects describe "${PROJECT}" --format='value(projectNumber)')"
PROFILE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
gcloud pubsub topics add-iam-policy-binding "${TOPIC}" \
  --project "${PROJECT}" \
  --member="serviceAccount:${PROFILE_SA}" \
  --role="roles/pubsub.publisher"

echo "==> Creating push subscription"
if gcloud pubsub subscriptions describe "${SUBSCRIPTION}" --project "${PROJECT}" >/dev/null 2>&1; then
  gcloud pubsub subscriptions update "${SUBSCRIPTION}" \
    --project "${PROJECT}" \
    --push-endpoint="${WORKER_URL}/" \
    --push-auth-service-account="${PUSH_SA}" \
    --dead-letter-topic="${DLQ_TOPIC}" \
    --max-delivery-attempts=5
else
  gcloud pubsub subscriptions create "${SUBSCRIPTION}" \
    --project "${PROJECT}" \
    --topic="${TOPIC}" \
    --push-endpoint="${WORKER_URL}/" \
    --push-auth-service-account="${PUSH_SA}" \
    --dead-letter-topic="${DLQ_TOPIC}" \
    --max-delivery-attempts=5 \
    --ack-deadline=60
fi

echo "==> Granting Cloud Run Jobs invoker to scheduler SA"
gcloud projects add-iam-policy-binding "${PROJECT}" \
  --member="serviceAccount:${SCHEDULER_SA}" \
  --role="roles/run.developer"

echo "==> Creating nightly backfill scheduler job (if missing)"
JOB_URI="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT}/jobs/embedding-backfill:run"
if gcloud scheduler jobs describe embedding-backfill-nightly \
    --project "${PROJECT}" --location "${REGION}" >/dev/null 2>&1; then
  gcloud scheduler jobs update http embedding-backfill-nightly \
    --project "${PROJECT}" \
    --location "${REGION}" \
    --schedule="0 3 * * *" \
    --uri="${JOB_URI}" \
    --http-method=POST \
    --oauth-service-account-email="${SCHEDULER_SA}"
else
  gcloud scheduler jobs create http embedding-backfill-nightly \
    --project "${PROJECT}" \
    --location "${REGION}" \
    --schedule="0 3 * * *" \
    --uri="${JOB_URI}" \
    --http-method=POST \
    --oauth-service-account-email="${SCHEDULER_SA}"
fi

echo ""
echo "Provisioning complete."
echo "  Worker URL: ${WORKER_URL}"
echo "  Topic: ${TOPIC}"
echo "  Subscription: ${SUBSCRIPTION}"
echo ""
echo "One-time catch-up backfill:"
echo "  gcloud run jobs execute embedding-backfill --project ${PROJECT} --region ${REGION}"
