#!/usr/bin/env bash
# ==============================================================================
# Database Initialization Script
# ==============================================================================
set -euo pipefail

echo "==> Running database initialization..."

# Run Alembic migrations to head
if command -v alembic >/dev/null 2>&1; then
    echo "Applying migrations via local Alembic..."
    cd "$(dirname "$0")/../../backend" && alembic upgrade head
else
    echo "Applying migrations via Docker..."
    docker compose exec backend alembic upgrade head
fi

echo "==> Database initialization complete."
