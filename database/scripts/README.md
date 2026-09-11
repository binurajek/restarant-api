# Database Utility Scripts

Utility bash scripts for development and CI/CD pipelines.

## Scripts
- `init_db.sh`: Applies all pending migrations up to `head`.
- `wait_for_db.sh`: Polls PostgreSQL until the socket is accepting client connections.
