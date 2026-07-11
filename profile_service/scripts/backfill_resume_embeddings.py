#!/usr/bin/env python3
"""Deprecated: use embedding-backfill Cloud Run Job instead.

See scripts/provision-embedding-infra.sh and DEPLOYMENT.md (Embedding Worker section).
"""

raise SystemExit(
    "This script has been replaced by the embedding-backfill Cloud Run Job. "
    "Run: gcloud run jobs execute embedding-backfill --region us-central1"
)
