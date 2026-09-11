.PHONY: help install up down restart logs test lint format typecheck security migrate migration clean db-seed

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "Restaurant Platform - Management Commands"
	@echo "========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# ------------------------------------------------------------------------------
# Environment & Installation
# ------------------------------------------------------------------------------
install: ## Install dependencies in backend virtual environment
	@echo "Installing backend dependencies..."
	cd backend && python3 -m pip install --upgrade pip && pip install -e ".[dev]"

env: ## Create .env from .env.example if not present
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example"; else echo ".env already exists"; fi

# ------------------------------------------------------------------------------
# Docker Stack Management
# ------------------------------------------------------------------------------
up: env ## Start all Docker services in the background (Postgres, Redis, Backend)
	docker compose up --build -d
	@echo "Stack running: Backend: http://localhost:8000 (Docs: http://localhost:8000/docs)"

down: ## Stop all Docker services
	docker compose down

restart: ## Restart all Docker services
	docker compose restart

logs: ## Tail logs from all Docker containers
	docker compose logs -f

logs-backend: ## Tail logs from the backend container
	docker compose logs -f backend

# ------------------------------------------------------------------------------
# Testing & Code Quality
# ------------------------------------------------------------------------------
test: ## Run unit, integration, and API tests
	@if [ -d "backend/.venv" ] || command -v pytest >/dev/null 2>&1; then \
		cd backend && pytest -v; \
	else \
		docker compose run --rm backend pytest -v; \
	fi

lint: ## Run Ruff linter
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check backend; \
	else \
		docker compose run --rm backend ruff check app tests; \
	fi

format: ## Run Ruff auto-formatting
	@if command -v ruff >/dev/null 2>&1; then \
		ruff format backend && ruff check --fix backend; \
	else \
		docker compose run --rm backend ruff format app tests; \
	fi

typecheck: ## Run MyPy static type checking
	@if command -v mypy >/dev/null 2>&1; then \
		cd backend && mypy app; \
	else \
		docker compose run --rm backend mypy app; \
	fi

security: ## Run Bandit security scan and pip-audit vulnerability check
	@if command -v bandit >/dev/null 2>&1; then \
		cd backend && bandit -r app/ -s B106,B107 && pip-audit; \
	else \
		docker compose run --rm backend sh -c "bandit -r app/ -s B106,B107 && pip-audit"; \
	fi

# ------------------------------------------------------------------------------
# Database & Migrations
# ------------------------------------------------------------------------------
migrate: ## Apply database migrations to head
	@if docker compose ps backend | grep -q "Up"; then \
		docker compose exec backend alembic upgrade head; \
	else \
		docker compose run --rm backend alembic upgrade head; \
	fi

migration: ## Generate a new Alembic migration (usage: make migration m="add users table")
	@if [ -z "$(m)" ]; then echo "Error: Migration message required. Usage: make migration m=\"message\""; exit 1; fi
	@if docker compose ps backend | grep -q "Up"; then \
		docker compose exec backend alembic revision --autogenerate -m "$(m)"; \
	else \
		docker compose run --rm backend alembic revision --autogenerate -m "$(m)"; \
	fi

db-seed: ## Seed database with development data
	docker compose exec -T postgres psql -U postgres -d restaurant_db < database/seeds/01_initial_seed.sql
	@echo "Database seeded successfully."

# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------
clean: ## Remove caches, build artifacts, and docker volumes
	docker compose down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/build backend/dist backend/*.egg-info
	@echo "Clean completed."
