# Database Seeds

This folder contains seed SQL files for populating local and testing environments with representative dataset fixtures.

## Available Seeds
- `01_initial_seed.sql`: Creates platform admin, restaurant owner, demo restaurant (*Osteria Del Sole*), 2 branches, dinner menu, categories, and 5 menu items.

## Usage
Seed the local Docker database:
```bash
make db-seed
```

Or execute directly via `psql`:
```bash
psql $DATABASE_URL -f database/seeds/01_initial_seed.sql
```
