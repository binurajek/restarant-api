#!/usr/bin/env bash
# ==============================================================================
# Wait For PostgreSQL Readiness
# ==============================================================================
set -euo pipefail

HOST="${POSTGRES_SERVER:-localhost}"
PORT="${POSTGRES_PORT:-5432}"
USER="${POSTGRES_USER:-postgres}"

echo "==> Waiting for PostgreSQL at ${HOST}:${PORT}..."

MAX_RETRIES=30
COUNT=0

until pg_isready -h "$HOST" -p "$PORT" -U "$USER" >/dev/null 2>&1 || [ $COUNT -eq $MAX_RETRIES ]; do
    echo "PostgreSQL is unavailable - sleeping 1s (attempt $((COUNT+1))/$MAX_RETRIES)..."
    sleep 1
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Error: Timed out waiting for PostgreSQL."
    exit 1
fi

echo "==> PostgreSQL is up and accepting connections."
