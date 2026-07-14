#!/usr/bin/env bash
# Deploy profile_service, recommendation_service, and embedding_worker to Google Cloud Run.
#
# Prerequisites:
#   - gcloud CLI authenticated, billing enabled, APIs enabled
#   - Docker running (Apple Silicon: builds linux/amd64 for Cloud Run)
#   - Secrets in Secret Manager: database-url, gemini-api-key, profile-api-key,
#     azure-storage-connection-string, resend-api-key
#   - HF_TOKEN env var set when building embedding_worker (model download at build time)
#   - Run scripts/provision-embedding-infra.sh once to create Pub/Sub + scheduler
#
# Usage:
#   GCP_PROJECT=your-project-id GCP_REGION=us-central1 HF_TOKEN=hf_... ./scripts/deploy-cloud-run.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
REPO="${ARTIFACT_REPO:-job-crawler}"
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}"

# Production frontends — job-scout.dev is primary; keep legacy during transition.
CORS_ORIGINS="https://job-scout.dev"

# Docker folder name (underscore) -> Cloud Run service name (dash)
cloud_run_name() {
  echo "${1//_/-}"
}

deploy_service() {
  local service_dir="$1"
  local run_name
  run_name="$(cloud_run_name "${service_dir}")"
  local image="${REGISTRY}/${service_dir}:latest"

  echo "==> Building ${service_dir} (linux/amd64)"
  docker build --platform linux/amd64 \
    --build-arg "SERVICE=${service_dir}" \
    -t "${image}" \
    "${ROOT}"

  echo "==> Pushing ${image}"
  docker push "${image}"

  echo "==> Deploying ${run_name} to Cloud Run"
  shift
  gcloud run deploy "${run_name}" \
    --project "${PROJECT}" \
    --region "${REGION}" \
    --image "${image}" \
    --platform managed \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 3 \
    --cpu 1 \
    --memory "$([ "${service_dir}" = "profile_service" ] && echo 1Gi || echo 512Mi)" \
    "$@"
}

deploy_embedding_worker() {
  local image="${REGISTRY}/embedding_worker:latest"

  if [[ -z "${HF_TOKEN:-}" ]]; then
    echo "WARNING: HF_TOKEN is not set — embedding_worker build may fail without Hugging Face auth."
  fi

  echo "==> Building embedding_worker (linux/amd64)"
  docker build --platform linux/amd64 \
    --build-arg "HF_TOKEN=${HF_TOKEN:-}" \
    -f "${ROOT}/embedding_worker/Dockerfile" \
    -t "${image}" \
    "${ROOT}"

  echo "==> Pushing ${image}"
  docker push "${image}"

  echo "==> Deploying embedding-worker to Cloud Run"
  gcloud run deploy embedding-worker \
    --project "${PROJECT}" \
    --region "${REGION}" \
    --image "${image}" \
    --platform managed \
    --no-allow-unauthenticated \
    --min-instances 0 \
    --max-instances 3 \
    --cpu 1 \
    --memory 1Gi \
    --timeout 300 \
    --set-secrets "DATABASE_URL=database-url:latest" \
    --set-env-vars "HF_HUB_OFFLINE=1,TRANSFORMERS_OFFLINE=1,LOG_LEVEL=INFO"

  if gcloud run jobs describe embedding-backfill \
      --project "${PROJECT}" --region "${REGION}" >/dev/null 2>&1; then
    echo "==> Updating embedding-backfill Cloud Run Job"
    gcloud run jobs update embedding-backfill \
      --project "${PROJECT}" \
      --region "${REGION}" \
      --image "${image}" \
      --command "python" \
      --args=-m,app.backfill \
      --memory 1Gi \
      --cpu 1 \
      --set-secrets "DATABASE_URL=database-url:latest" \
      --set-env-vars "HF_HUB_OFFLINE=1,TRANSFORMERS_OFFLINE=1,LOG_LEVEL=INFO"
  else
    echo "==> Creating embedding-backfill Cloud Run Job"
    gcloud run jobs create embedding-backfill \
      --project "${PROJECT}" \
      --region "${REGION}" \
      --image "${image}" \
      --command "python" \
      --args=-m,app.backfill \
      --memory 1Gi \
      --cpu 1 \
      --set-secrets "DATABASE_URL=database-url:latest" \
      --set-env-vars "HF_HUB_OFFLINE=1,TRANSFORMERS_OFFLINE=1,LOG_LEVEL=INFO"
  fi
}

# Ensure Artifact Registry repo exists
gcloud artifacts repositories describe "${REPO}" \
  --project "${PROJECT}" \
  --location "${REGION}" >/dev/null 2>&1 \
  || gcloud artifacts repositories create "${REPO}" \
       --project "${PROJECT}" \
       --location "${REGION}" \
       --repository-format docker

gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

deploy_service profile_service \
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest,API_KEY=profile-api-key:latest,AZURE_STORAGE_CONNECTION_STRING=azure-storage-connection-string:latest,RESEND_API_KEY=resend-api-key:latest" \
  --set-env-vars "RESUME_STORAGE_BACKEND=azure,AZURE_STORAGE_CONTAINER=resumes,CORS_ORIGINS=${CORS_ORIGINS},EMAIL_FROM=Job Scout <notifications@job-scout.dev>,GCP_PROJECT=${PROJECT},EMBEDDING_REQUESTS_TOPIC=embedding-requests,EMBEDDING_PUBLISH_ENABLED=true"

deploy_service recommendation_service \
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest,REDIS_URL=redis-url:latest" \
  --set-env-vars "ENABLE_NOTIFICATION_SCHEDULER=false,CORS_ORIGINS=${CORS_ORIGINS},RECOMMENDATION_RRF_ENABLED=true,RECOMMENDATION_PAGE_SIZE=40,RECOMMENDATION_CACHE_TTL_SECONDS=1800"

deploy_embedding_worker

echo ""
echo "Deploy complete. Service URLs:"
gcloud run services describe profile-service \
  --project "${PROJECT}" --region "${REGION}" --format='value(status.url)'
gcloud run services describe recommendation-service \
  --project "${PROJECT}" --region "${REGION}" --format='value(status.url)'
gcloud run services describe embedding-worker \
  --project "${PROJECT}" --region "${REGION}" --format='value(status.url)'
echo ""
echo "CORS_ORIGINS=${CORS_ORIGINS} (set on both Cloud Run services)"
echo ""
echo "Next steps:"
echo "  1. Run ./scripts/provision-embedding-infra.sh (once) to wire Pub/Sub push subscription"
echo "  2. Grant profile-service SA roles/pubsub.publisher on embedding-requests topic"
echo "  3. One-time backfill: gcloud run jobs execute embedding-backfill --project ${PROJECT} --region ${REGION}"
echo ""
echo "Set Vercel env vars:"
echo "  NEXT_PUBLIC_RECOMMENDATION_API_URL=<recommendation-service URL>"
echo "  PROFILE_API_URL=<profile-service URL>"
