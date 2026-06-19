#!/usr/bin/env bash
# Deploy profile_service and recommendation_service API to Google Cloud Run.
#
# Prerequisites:
#   - gcloud CLI authenticated, billing enabled, APIs enabled
#   - Docker running (Apple Silicon: builds linux/amd64 for Cloud Run)
#   - Secrets in Secret Manager: database-url, gemini-api-key, profile-api-key,
#     supabase-url, supabase-service-role-key
#
# Usage:
#   GCP_PROJECT=your-project-id GCP_REGION=us-central1 ./scripts/deploy-cloud-run.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
REPO="${ARTIFACT_REPO:-job-crawler}"
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}"

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
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest,API_KEY=profile-api-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-service-role-key:latest" \
  --set-env-vars "RESUME_STORAGE_BACKEND=supabase,SUPABASE_STORAGE_BUCKET=resumes"

deploy_service recommendation_service \
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest" \
  --set-env-vars "ENABLE_NOTIFICATION_SCHEDULER=false"

echo ""
echo "Deploy complete. Service URLs:"
gcloud run services describe profile-service \
  --project "${PROJECT}" --region "${REGION}" --format='value(status.url)'
gcloud run services describe recommendation-service \
  --project "${PROJECT}" --region "${REGION}" --format='value(status.url)'
echo ""
echo "Set Vercel env vars:"
echo "  NEXT_PUBLIC_RECOMMENDATION_API_URL=<recommendation-service URL>"
echo "  PROFILE_API_URL=<profile-service URL>"
