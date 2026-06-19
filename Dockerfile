# Build: docker build --build-arg SERVICE=profile_service -t profile-service .
# Build: docker build --build-arg SERVICE=recommendation_service -t recommendation-service .
FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
ARG SERVICE=profile_service
ENV SERVICE=${SERVICE}

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

COPY ${SERVICE}/app ./app
COPY ${SERVICE}/alembic ./alembic
COPY ${SERVICE}/alembic.ini ./alembic.ini

ENV PORT=8080
EXPOSE 8080

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
