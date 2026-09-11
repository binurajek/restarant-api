# Restaurant Platform - Backend Service

FastAPI-powered asynchronous backend service for the Restaurant Platform.

## Features
- **Modern Python**: Built with Python 3.13+
- **Async API**: FastAPI with Uvicorn ASGI server
- **Database**: PostgreSQL / Neon via SQLAlchemy 2.x and asyncpg
- **Schema Migrations**: Alembic async runner
- **Security**: Argon2id password hashing, JWT token authentication
- **Quality & Testing**: Ruff, MyPy, Bandit, pip-audit, Pytest, HTTPX

## Quick Start (Local)

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -e ".[dev]"
```

### 3. Run development server
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure
```
app/
├── api/v1/         # API routes
├── core/           # Configuration, security, logging, constants
├── database/       # SQLAlchemy 2.x async engine and session dependencies
├── models/         # ORM declarative models
├── schemas/        # Pydantic v2 schemas
├── repositories/   # Data access layer
├── services/       # Business logic layer
├── middleware/     # Request ID, logging, and error handling
├── integrations/   # Interfaces for AI, payments, maps, notifications
└── tasks/          # Background tasks
```
