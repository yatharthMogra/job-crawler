#!/usr/bin/env bash
# Deploy profile_service and recommendation_service API to Google Cloud Run.
#
# Prerequisites:
#   - gcloud CLI authenticated
#   - GCP_PROJECT, GCP_REGION, ARTIFACT_REPO env vars set (or pass as args)
#   - Secrets created in Secret Manager: database-url, gemini-api-key, profile-api-key
#
# Usage:
#   GCP_PROJECT=my-project GCP_REGION=us-central1 ./scripts/deploy-cloud-run.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
REPO="${ARTIFACT_REPO:-job-crawler}"
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT}/${REPO}"

deploy_service() {
  local service="$1"
  local image="${REGISTRY}/${service}:latest"
  local extra_env="${2:-}"

  echo "==> Building ${service}"
  docker build --build-arg "SERVICE=${service}" -t "${image}" "${ROOT}"

  echo "==> Pushing ${image}"
  docker push "${image}"

  echo "==> Deploying ${service} to Cloud Run"
  # shellcheck disable=SC2086
  gcloud run deploy "${service}" \
    --project "${PROJECT}" \
    --region "${REGION}" \
    --image "${image}" \
    --platform managed \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 3 \
    --cpu 1 \
    --memory "$([ "${service}" = "profile_service" ] && echo 1Gi || echo 512Mi)" \
    --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest" \
    ${extra_env}
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

deploy_service "profile_service" \
  "--set-secrets API_KEY=profile-api-key:latest --set-env-vars RESUME_STORAGE_BACKEND=supabase,SUPABASE_STORAGE_BUCKET=resumes --update-secrets SUPABASE_URL=supabase-url:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-service-role-key:latest"

deploy_service "recommendation_service" \
  "--set-env-vars ENABLE_NOTIFICATION_SCHEDULER=false"

echo ""
echo "Deploy complete. Set Vercel env vars:"
echo "  NEXT_PUBLIC_RECOMMENDATION_API_URL=<recommendation_service URL>"
echo "  PROFILE_API_URL=<profile_service URL>"
