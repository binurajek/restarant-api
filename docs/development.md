# Development Guide

## 1. Prerequisites
- **Docker & Docker Compose** (Recommended for local orchestration)
- **Python 3.13+** (if running natively)
- **Git**
- **Make**

---

## 2. Quickstart with Docker Compose

### Step 1: Initialize Environment
```bash
cp .env.example .env
```

### Step 2: Start Services
```bash
make up
```
This builds the Python backend container and launches:
- `backend`: FastAPI API server on `http://localhost:8000`
- `postgres`: PostgreSQL 16 database on `localhost:5432`
- `redis`: Redis 7 cache on `localhost:6379`

### Step 3: Run Migrations & Seed Data
```bash
make migrate
make db-seed
```

### Step 4: Verify Health
```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/database
```

---

## 3. Local Native Development (Without Docker)

### 1. Create Virtual Environment
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure Environment
Set `DATABASE_URL` in `.env` to point to your local PostgreSQL instance:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/restaurant_db
```

### 3. Run FastAPI with Hot Reload
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 4. Code Quality & Testing Commands

| Task | Command | Description |
|---|---|---|
| **Run Tests** | `make test` | Runs unit, integration, and API tests via Pytest |
| **Lint** | `make lint` | Runs Ruff linter checks |
| **Format** | `make format` | Formats code with Ruff |
| **Type Check** | `make typecheck` | Static type checks with MyPy |
| **Security** | `make security` | Bandit security scan and pip-audit vulnerability check |
| **Migrations** | `make migrate` | Applies pending Alembic migrations |
| **New Migration** | `make migration m="title"` | Autogenerates Alembic migration |
| **Seed** | `make db-seed` | Seeds database with development data |
| **Clean** | `make clean` | Removes containers, volumes, and caches |
