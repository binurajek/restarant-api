#!/usr/bin/env bash
# ==============================================================================
# Run Linters and Type Checks
# ==============================================================================
set -euo pipefail

echo "==> Running Ruff Lint..."
if command -v ruff >/dev/null 2>&1; then
    ruff check backend
    echo "==> Running Ruff Format Check..."
    ruff format --check backend
    echo "==> Running MyPy Type Check..."
    cd "$(dirname "$0")/../backend" && mypy app
else
    docker compose run --rm backend ruff check app tests
    docker compose run --rm backend ruff format --check app tests
    docker compose run --rm backend mypy app
fi
echo "==> Code quality checks passed."
