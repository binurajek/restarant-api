#!/usr/bin/env bash
# ==============================================================================
# Run All Test Suites
# ==============================================================================
set -euo pipefail

echo "==> Running pytest test suite..."
if command -v pytest >/dev/null 2>&1; then
    cd "$(dirname "$0")/../backend" && pytest -v
else
    docker compose run --rm backend pytest -v
fi
