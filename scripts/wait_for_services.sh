#!/usr/bin/env bash
# ==============================================================================
# Wait for Backend and Database Health
# ==============================================================================
set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000/api/v1/health}"
echo "==> Waiting for backend at ${BACKEND_URL}..."

MAX_RETRIES=30
COUNT=0

until curl -s -f "$BACKEND_URL" >/dev/null 2>&1 || [ $COUNT -eq $MAX_RETRIES ]; do
    echo "Backend is starting - sleeping 2s (attempt $((COUNT+1))/$MAX_RETRIES)..."
    sleep 2
    COUNT=$((COUNT+1))
done

if [ $COUNT -eq $MAX_RETRIES ]; then
    echo "Error: Timed out waiting for Backend."
    exit 1
fi

echo "==> Backend is healthy and ready."
