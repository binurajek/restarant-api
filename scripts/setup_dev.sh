#!/usr/bin/env bash
# ==============================================================================
# Development Environment Setup Script
# ==============================================================================
set -euo pipefail

echo "===================================================="
echo " Setting up Restaurant Platform Development Stack   "
echo "===================================================="

# 1. Ensure .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# 2. Check Docker availability
if ! command -v docker >/dev/null 2>&1; then
    echo "Warning: Docker is not installed or not in PATH."
else
    echo "Docker found: $(docker --version)"
fi

echo ""
echo "Setup complete! Start services with:"
echo "  make up"
echo "or:"
echo "  docker compose up --build"
