#!/usr/bin/env bash
set -euo pipefail

echo "[dev-with-db] Starting Nephthys in dev mode with local Postgres"

if ! command -v docker >/dev/null 2>&1; then
  echo "[dev-with-db] ERROR: Docker is not installed or not in PATH."
  echo "[dev-with-db] Please install Docker Desktop and retry."
  exit 1
fi

# Start or create the Postgres container
if docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres$'; then
  if ! docker ps --format '{{.Names}}' | grep -q '^hh-postgres$'; then
    echo "[dev-with-db] Starting existing Postgres container 'hh-postgres'..."
    if ! docker start hh-postgres >/dev/null 2>&1; then
      echo "[dev-with-db] Port 5432 appears in use; attempting to run Postgres on 5433..."
      if ! docker ps -a --format '{{.Names}}' | grep -q '^hh-postgres-5433$'; then
        docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
      else
        docker start hh-postgres-5433 >/dev/null || true
      fi
      export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
      echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
    fi
  else
    echo "[dev-with-db] Postgres container 'hh-postgres' is already running."
  fi
else
  echo "[dev-with-db] Creating Postgres container 'hh-postgres'..."
  if ! docker run --name hh-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres >/dev/null 2>&1; then
    echo "[dev-with-db] Port 5432 appears in use; creating 'hh-postgres-5433' on 5433..."
    docker run --name hh-postgres-5433 -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres >/dev/null
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/nephthys"
    echo "[dev-with-db] Using DATABASE_URL=${DATABASE_URL}"
  fi
fi

# Wait briefly for Postgres to accept connections
echo "[dev-with-db] Waiting for Postgres to be ready..."
DB_PORT="${DATABASE_URL##*:@localhost:}"
DB_PORT="${DB_PORT%%/*}"
DB_PORT="${DB_PORT:-5432}"
for i in {1..20}; do
  if nc -z localhost "${DB_PORT}" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "[dev-with-db] Generating Prisma client..."
uv run prisma generate

echo "[dev-with-db] Pushing Prisma schema..."
uv run prisma db push || {
  echo "[dev-with-db] WARNING: prisma db push failed (database may not be fully ready yet). Retrying once..."
  sleep 2
  uv run prisma db push
}

echo "[dev-with-db] Starting app (uvicorn via script)..."
uv run nephthys
