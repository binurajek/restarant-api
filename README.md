# Restaurant Platform

> Production-grade backend API and database architecture foundation for a multi-channel restaurant discovery, digital menu, QR ordering, table reservations, and management platform.

[![CI Pipeline](https://github.com/organization/restaurant-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/organization/restaurant-platform/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791.svg)](https://www.postgresql.org)
[![Neon](https://img.shields.io/badge/Neon-Compatible-00E599.svg)](https://neon.tech)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Architecture Overview

The repository is structured as a unified **monorepo** containing two decoupled projects:
1. **Backend Project (`backend/`)**: Python 3.13+ asynchronous REST API powered by FastAPI, SQLAlchemy 2.x, asyncpg, and Pydantic v2.
2. **Database Project (`database/`)**: PostgreSQL schema blueprints, Alembic migrations, database seeds, and operational tooling supporting both local Docker and serverless Neon PostgreSQL.

```mermaid
graph LR
    subgraph Clients
        Mobile["iOS / Android Apps"]
        Web["Customer & Restaurant Web Portals"]
    end

    subgraph Backend ["FastAPI Backend (/api/v1)"]
        Router["Routers"] --> Service["Service Layer"]
        Service --> Repo["Repository Layer"]
        Repo --> ORM["SQLAlchemy 2.x Async"]
    end

    subgraph Data ["Data & Cache"]
        ORM --> DB[("PostgreSQL / Neon")]
        Service --> Cache[("Redis 7 Cache")]
    end

    Mobile --> Backend
    Web --> Backend
```

---

## 2. Repository Structure

```text
restaurant-platform/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints (health, auth, users, restaurants, menus, etc.)
│   │   ├── core/            # Configuration, security (Argon2id, JWT), logging, enums
│   │   ├── database/        # Async engine, sessionmaker, FastAPI dependencies
│   │   ├── models/          # Declarative SQLAlchemy 2.x ORM models
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   ├── repositories/    # Isolated data access layer
│   │   ├── services/        # Business logic layer
│   │   ├── middleware/      # Request ID, performance logging, global error handler
│   │   ├── integrations/    # Extensible adapters for AI, payments, maps, notifications
│   │   └── tasks/           # Asynchronous job definitions
│   ├── tests/
│   │   ├── unit/            # Configuration, security, and schema unit tests
│   │   ├── integration/     # Database relationships and repository tests
│   │   ├── api/             # HTTP endpoint tests with httpx
│   │   └── conftest.py      # Async test fixtures and in-memory engine
│   ├── alembic/             # Async Alembic migrations
│   ├── pyproject.toml       # Dependencies, packaging, and tool configs
│   ├── Dockerfile           # Multi-stage production container
│   └── README.md
├── database/
│   ├── migrations/          # Migration instructions and history
│   ├── seeds/               # 01_initial_seed.sql (restaurants, users, menus)
│   ├── schema/              # Standalone DDL reference and domain roadmap
│   ├── scripts/             # Database initialization and readiness helpers
│   └── README.md
├── docker/
│   └── postgres/            # Container database extensions init script
├── docs/                    # In-depth architectural and developer documentation
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── development.md
│   └── security.md
├── scripts/                 # Monorepo automation scripts
├── .github/workflows/ci.yml # GitHub Actions CI (Ruff, MyPy, Pytest, Bandit, pip-audit)
├── .env.example             # Complete environment configuration template
├── .gitignore
├── docker-compose.yml       # Local development stack (Backend, Postgres, Redis)
├── Makefile                 # Developer CLI
├── README.md
└── LICENSE
```

---

## 3. Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Make](https://www.gnu.org/software/make/) (optional, commands can be run directly)

### 1. Launch Environment
```bash
make up
```
*Behind the scenes, this creates `.env`, builds the backend container, and starts FastAPI, PostgreSQL, and Redis.*

### 2. Run Database Migrations
```bash
make migrate
```

### 3. Seed Development Data
```bash
make db-seed
```

### 4. Verify Endpoints
- **Health Check**: `curl http://localhost:8000/api/v1/health`
- **Database Connectivity**: `curl http://localhost:8000/api/v1/health/database`
- **Interactive Swagger UI**: Open `http://localhost:8000/docs`
- **ReDoc**: Open `http://localhost:8000/redoc`

---

## 4. Development Workflow & Commands

| Command | Description |
|---|---|
| `make up` | Start backend, PostgreSQL, and Redis containers |
| `make down` | Stop all running containers |
| `make logs` | View real-time logs from all services |
| `make test` | Execute unit, integration, and API test suites |
| `make lint` | Run Ruff linter checks |
| `make format` | Automatically format code and sort imports |
| `make typecheck` | Run MyPy static type checking |
| `make security` | Run Bandit security scan and pip-audit vulnerability check |
| `make migrate` | Apply all pending database migrations |
| `make migration m="..."` | Generate a new Alembic migration revision |
| `make db-seed` | Populate database with realistic demo data |
| `make clean` | Stop containers, remove volumes, and purge cache files |

---

## 5. PostgreSQL & Neon Compatibility

The backend uses standard PostgreSQL connection strings and auto-normalizes driver schemes to `postgresql+asyncpg://`:

- **Local Development**: `postgresql+asyncpg://postgres:postgres@localhost:5432/restaurant_db`
- **Production (Neon)**: `postgresql+asyncpg://<user>:<password>@<ep-xyz>.eu-central-1.aws.neon.tech/restaurant_db?ssl=require`

No application code alterations are needed between local Docker and cloud Neon deployments.

---

## 6. Testing & Quality Assurance

All tests run using **Pytest** with asynchronous I/O and isolated in-memory testing engines:

```bash
make test
```

Code quality standards enforced in CI:
- **Linting & Formatting**: Ruff (target: Python 3.13)
- **Type Checking**: MyPy (strict type annotations)
- **Security Audits**: Bandit & pip-audit

---

## 7. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
