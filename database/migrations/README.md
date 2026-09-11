# Database Migrations

Database schema migrations are authored and executed through Alembic located in `backend/alembic/`.

## Migration Principles
1. **Never alter existing migration scripts that have been committed and applied in staging or production.**
2. **Every migration must define both `upgrade()` and `downgrade()` procedures.**
3. **Use explicit type mappings and constraint naming conventions.**
4. **Always run lint and tests after generating new migrations.**

## Commands
Apply migrations:
```bash
make migrate
```

Generate new migration based on SQLAlchemy model changes:
```bash
make migration m="describe change here"
```

Check current revision:
```bash
docker compose exec backend alembic current
```

Check migration history:
```bash
docker compose exec backend alembic history --verbose
```
