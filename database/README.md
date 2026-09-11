# Restaurant Platform — Database Project

PostgreSQL and Neon database configuration, schema foundation, migrations, seeds, and database engineering tooling.

## Overview
- **Production Host**: Neon PostgreSQL (Serverless, Branching, SSL)
- **Development Host**: Docker PostgreSQL (PostgreSQL 16 Alpine)
- **Migration Engine**: Alembic (asynchronous runner via `asyncpg`)
- **Primary Keys**: UUIDv4 (`uuid-ossp`, `pgcrypto`)
- **Timestamps**: UTC with timezone (`timestamptz`)
- **Monetary Values**: Exact `NUMERIC(10, 2)` (never floating point)

## Directory Structure
```
database/
├── migrations/      # Migration guides and version linkage
├── seeds/           # Development and staging seed SQL scripts
├── scripts/         # Automation shell scripts (healthcheck, init, seed)
├── schema/          # Pure SQL DDL schema definitions and domain catalog
└── README.md
```

## Neon PostgreSQL Setup (Production / Staging)
1. Create a Neon project on [neon.tech](https://neon.tech).
2. Copy the connection string provided in the Neon console.
3. Configure the `DATABASE_URL` in your environment (or `.env`):
   ```env
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@<neon-host>/<database>?ssl=require
   ```
4. Run migrations:
   ```bash
   make migrate
   ```

## Running Migrations Locally
Run all migrations up to `head`:
```bash
make migrate
```

Roll back one revision:
```bash
docker compose exec backend alembic downgrade -1
```

Generate new migration:
```bash
make migration m="add dietary preferences"
```

## Seeding Development Data
To populate the database with demo users, restaurants, branches, menus, categories, and items:
```bash
make db-seed
```
