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

### 4. Verify Endpoints & Interactive Testing
- **Health Check**: `curl http://localhost:8000/api/v1/health`
- **Database Connectivity**: `curl http://localhost:8000/api/v1/health/database`
- **Interactive Swagger UI**: Open `http://localhost:8000/docs` or `http://localhost:8000/swagger` (features interactive JWT **Authorize 🔓** modal, live latency metrics, and tag filtering)
- **ReDoc**: Open `http://localhost:8000/redoc`
- **Postman Collection**: Import [postman_collection.json](postman_collection.json) directly into Postman for automated end-to-end chaining and testing.

### 5. Ports & Services Reference Table

| Service | Container Name | Host Port | Container Port | Protocol | Access URL / Connection String |
|---|---|:---:|:---:|:---:|---|
| **FastAPI Backend (API)** | `restaurant_backend` | **`8000`** | `8000` | HTTP | `http://localhost:8000/api/v1` |
| **Interactive Swagger UI** | `restaurant_backend` | **`8000`** | `8000` | HTTP | `http://localhost:8000/docs` or `http://localhost:8000/swagger` |
| **ReDoc API Documentation** | `restaurant_backend` | **`8000`** | `8000` | HTTP | `http://localhost:8000/redoc` |
| **OpenAPI Schema (JSON)** | `restaurant_backend` | **`8000`** | `8000` | HTTP | `http://localhost:8000/openapi.json` |
| **PostgreSQL 16 Database** | `restaurant_postgres` | **`5432`** | `5432` | TCP | `postgresql://postgres:postgres@localhost:5432/restaurant_db` |
| **Redis 7 Cache** | `restaurant_redis` | **`6379`** | `6379` | TCP | `redis://localhost:6379/0` |

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

## 7. Developer Quickstart: Setup, Swagger UI & Postman Testing

Follow this guide to spin up the local environment and test all endpoints interactively or via automated Postman collections.

### 7.1 Local Project Setup

#### 1. Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/) installed and running.
- [Make](https://www.gnu.org/software/make/) (available by default on macOS and Linux).

#### 2. Launch Local Stack
Run the following commands in the root directory:
```bash
# 1. Start backend, PostgreSQL, and Redis containers in the background
make up

# 2. Run Alembic database migrations
make migrate

# 3. Populate database with realistic development seed data
make db-seed
```
*The stack will be up and running: Backend & Swagger UI on **port 8000**, PostgreSQL on **port 5432**, and Redis on **port 6379**.*

#### 3. Seeded Accounts for Testing
The seed script (`database/seeds/01_initial_seed.sql`) provisions the following accounts:
- **Admin**: `admin@restaurantplatform.com` / `Password123!` (role: `admin`)
- **Restaurant Owner**: `owner@osteriadelsole.com` / `Password123!` (role: `restaurant_owner`)
- **Demo Restaurant**: `Osteria Del Sole` (slug: `osteria-del-sole`)

---

### 7.2 Interactive API Testing with Swagger UI

FastAPI provides an interactive OpenAPI / Swagger UI preconfigured with JWT Bearer authentication, real-time tag filtering, and latency metrics.

1. **Access Swagger UI**:
   - Open your browser to `http://localhost:8000/docs` (or `http://localhost:8000/swagger`).
2. **Obtain a JWT Access Token**:
   - In Swagger UI, expand the **Authentication** section.
   - Click `POST /api/v1/auth/login` -> Click **Try it out**.
   - Input test credentials:
     ```json
     {
       "email": "owner@osteriadelsole.com",
       "password": "Password123!"
     }
     ```
   - Click **Execute** and copy the `access_token` string from the JSON response.
3. **Authorize in Swagger**:
   - Scroll to the top and click the green **Authorize 🔓** button.
   - Paste the token into the **Value** input field (without `Bearer ` prefix).
   - Click **Authorize** -> Click **Close**.
   - All locked endpoints now display the locked padlock 🔒 and will automatically include your `Authorization: Bearer <token>` header.
4. **Persistent Session & Observability**:
   - Authorization persists across browser page refreshes (`persistAuthorization: True`).
   - Every response displays its unique `X-Request-ID` and server latency in milliseconds.

---

### 7.3 Automated Testing with Postman Collection

A complete, production-grade Postman Collection is provided in the repository root: [`postman_collection.json`](postman_collection.json).

#### 1. Import into Postman
1. Open the [Postman Desktop App](https://www.postman.com/downloads/) or Web App.
2. Click **Import** in the top-left corner.
3. Drag and drop the [`postman_collection.json`](postman_collection.json) file from the project root (or browse to select it).
4. Click **Import**.

#### 2. Automatic Token & ID Chaining
The collection is preconfigured with Postman test scripts that automatically capture IDs and tokens so you never have to manually copy-paste:
- **Step 1: Authenticate**:
  - Open folder `2. Authentication` -> Select **Login (Obtain JWT Access & Refresh Tokens)**.
  - Click **Send**.
  - The embedded test script automatically parses the response and sets the collection variables `accessToken` and `refreshToken`.
- **Step 2: Run Endpoints**:
  - All subsequent requests in `Users`, `Restaurants`, `Menus`, and `Menu Items` automatically inherit `{{accessToken}}`.
  - Creating a restaurant auto-populates `{{restaurantId}}` and `{{restaurantSlug}}`.
  - Creating a menu auto-populates `{{menuId}}` and `{{categoryId}}`.
  - Creating a menu item auto-populates `{{menuItemId}}`.
- **Step 3: Run Full Collection Runner**:
  - Right-click the **Restaurant Platform API** collection in Postman -> Click **Run collection**.
  - Click **Run Restaurant Platform API** to execute the entire end-to-end flow with status assertions in seconds.

---

### 7.4 Mobile Application Integration Guide
For mobile developers building iOS and Android applications for this backend:
- Refer to the exhaustive [MOBILE_APP_PLAN.md](MOBILE_APP_PLAN.md) in the project root for screen-by-screen API mappings, dual-token refresh interceptor sequence diagrams, offline caching strategy, and Dart/TypeScript type models.

---

## 8. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

