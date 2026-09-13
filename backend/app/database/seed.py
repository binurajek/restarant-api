import asyncio
from pathlib import Path

from alembic.config import Config
from sqlalchemy import text

from alembic import command
from app.core.logging import get_logger
from app.database.session import AsyncSessionLocal

logger = get_logger("app.database.seed")

INITIAL_SEED_SQL = """
-- 1. Insert Initial Platform Users (Password: "Password123!")
INSERT INTO users (id, email, hashed_password, full_name, phone, role, status, is_active, is_verified, created_at, updated_at)
VALUES
  (
    'a0000000-0000-0000-0000-000000000001',
    'admin@restaurantplatform.com',
    '$argon2id$v=19$m=65536,t=3,p=4$epEEYogk8xTOeChU2cWeBQ$L7N4xvQdX/WX7IA1LiQ/lkRgpcEfw8tR7H0zz9jLgog',
    'Platform Administrator',
    '+15550000001',
    'admin',
    'active',
    true,
    true,
    NOW(),
    NOW()
  ),
  (
    'a0000000-0000-0000-0000-000000000002',
    'owner@osteriadelsole.com',
    '$argon2id$v=19$m=65536,t=3,p=4$epEEYogk8xTOeChU2cWeBQ$L7N4xvQdX/WX7IA1LiQ/lkRgpcEfw8tR7H0zz9jLgog',
    'Giovanni Rossi',
    '+15550000002',
    'restaurant_owner',
    'active',
    true,
    true,
    NOW(),
    NOW()
  ),
  (
    'a0000000-0000-0000-0000-000000000003',
    'customer@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$epEEYogk8xTOeChU2cWeBQ$L7N4xvQdX/WX7IA1LiQ/lkRgpcEfw8tR7H0zz9jLgog',
    'Jane Doe',
    '+15550000003',
    'customer',
    'active',
    true,
    true,
    NOW(),
    NOW()
  )
ON CONFLICT (email) DO NOTHING;

-- 2. Insert Demo Restaurant (Linked to owner Giovanni Rossi)
INSERT INTO restaurants (id, name, slug, description, logo_url, cover_image_url, status, is_active, owner_id, created_at, updated_at)
VALUES
  (
    'b0000000-0000-0000-0000-000000000001',
    'Osteria Del Sole',
    'osteria-del-sole',
    'Handmade artisanal pasta, wood-fired seasonal dishes, and regional Italian wines.',
    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=200',
    'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200',
    'active',
    true,
    'a0000000-0000-0000-0000-000000000002',
    NOW(),
    NOW()
  )
ON CONFLICT (slug) DO NOTHING;

-- 3. Insert Restaurant Branches (Linked to Osteria Del Sole)
INSERT INTO restaurant_branches (id, restaurant_id, name, address_line, city, state_or_province, postal_code, country_code, latitude, longitude, phone, is_active, created_at, updated_at)
VALUES
  (
    'c0000000-0000-0000-0000-000000000001',
    'b0000000-0000-0000-0000-000000000001',
    'Downtown Historic Quarter',
    '450 Market Street',
    'San Francisco',
    'CA',
    '94105',
    'US',
    37.7891710,
    -122.4014490,
    '+15551234567',
    true,
    NOW(),
    NOW()
  ),
  (
    'c0000000-0000-0000-0000-000000000002',
    'b0000000-0000-0000-0000-000000000001',
    'Marina District Waterfront',
    '2100 Chestnut Street',
    'San Francisco',
    'CA',
    '94123',
    'US',
    37.8003190,
    -122.4371490,
    '+15559876543',
    true,
    NOW(),
    NOW()
  )
ON CONFLICT (id) DO NOTHING;

-- 4. Insert Menu (Linked to Osteria Del Sole)
INSERT INTO menus (id, restaurant_id, name, description, status, is_active, created_at, updated_at)
VALUES
  (
    'd0000000-0000-0000-0000-000000000001',
    'b0000000-0000-0000-0000-000000000001',
    'Dinner & Evening Menu',
    'Seasonal dinner offerings, served daily from 5:00 PM to 11:00 PM.',
    'active',
    true,
    NOW(),
    NOW()
  )
ON CONFLICT (id) DO NOTHING;

-- 5. Insert Categories (Linked to Dinner & Evening Menu)
INSERT INTO menu_categories (id, menu_id, name, description, display_order, created_at, updated_at)
VALUES
  ('e0000000-0000-0000-0000-000000000001', 'd0000000-0000-0000-0000-000000000001', 'Antipasti', 'Starters and sharing platters', 1, NOW(), NOW()),
  ('e0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000001', 'Primi Piatti', 'Fresh house-made pasta', 2, NOW(), NOW()),
  ('e0000000-0000-0000-0000-000000000003', 'd0000000-0000-0000-0000-000000000001', 'Secondi', 'Meats and wild seafood', 3, NOW(), NOW()),
  ('e0000000-0000-0000-0000-000000000004', 'd0000000-0000-0000-0000-000000000001', 'Dolci', 'Desserts and sweets', 4, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- 6. Insert Menu Items (Linked to Categories with Exact Pricing)
INSERT INTO menu_items (id, category_id, name, description, price, currency, is_available, calories, preparation_time_minutes, created_at, updated_at)
VALUES
  (
    'f0000000-0000-0000-0000-000000000001',
    'e0000000-0000-0000-0000-000000000001',
    'Burrata Pugliese',
    'Creamy Puglia burrata, heirloom cherry tomatoes, cold-pressed olive oil, aged balsamic glaze.',
    16.50,
    'USD',
    true,
    420,
    10,
    NOW(),
    NOW()
  ),
  (
    'f0000000-0000-0000-0000-000000000002',
    'e0000000-0000-0000-0000-000000000002',
    'Tagliolini al Tartufo',
    'Hand-cut egg ribbon pasta, cultured mountain butter, fresh shaved black summer truffle.',
    28.00,
    'USD',
    true,
    680,
    15,
    NOW(),
    NOW()
  ),
  (
    'f0000000-0000-0000-0000-000000000003',
    'e0000000-0000-0000-0000-000000000002',
    'Rigatoni all''Amatriciana',
    'Crispy Guanciale di Amatrice, San Marzano tomato reduction, Pecorino Romano DOP.',
    22.50,
    'USD',
    true,
    740,
    14,
    NOW(),
    NOW()
  ),
  (
    'f0000000-0000-0000-0000-000000000004',
    'e0000000-0000-0000-0000-000000000003',
    'Branzino al Forno',
    'Pan-roasted Mediterranean sea bass, sautéed baby spinach, saffron emulsion, capers.',
    34.00,
    'USD',
    true,
    510,
    22,
    NOW(),
    NOW()
  ),
  (
    'f0000000-0000-0000-0000-000000000005',
    'e0000000-0000-0000-0000-000000000004',
    'Tiramisù Tradizionale',
    'Savoiardi soaked in espresso, Zabaglione mascarpone mousse, Valrhona dark cocoa powder.',
    12.00,
    'USD',
    true,
    450,
    5,
    NOW(),
    NOW()
  )
ON CONFLICT (id) DO NOTHING;
"""


def run_alembic_migrations() -> None:
    """Run Alembic migrations to head programmatically."""
    ini_path = Path(__file__).resolve().parent.parent.parent / "alembic.ini"
    if ini_path.exists():
        alembic_cfg = Config(str(ini_path))
        command.upgrade(alembic_cfg, "head")


async def seed_database_if_empty() -> bool:
    """Verify if database is unseeded; if empty, seed with relational demo data."""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text("SELECT COUNT(*) FROM users;"))
            count = result.scalar() or 0
            if count > 0:
                logger.info("Database already seeded (%d users found). Skipping auto-seed.", count)
                return False

            logger.info("Database is empty. Automatically applying initial relational seed data...")
            for statement in INITIAL_SEED_SQL.split(";"):
                cleaned = statement.strip()
                if cleaned:
                    await session.execute(text(cleaned))
            await session.commit()
            logger.info("Initial relational seed data successfully applied.")
            return True
        except Exception as exc:
            logger.warning("Auto-seed check encountered an issue: %s", exc)
            await session.rollback()
            return False


async def init_and_seed_database() -> bool:
    """Ensure database schema is migrated and relational seed data is populated."""
    try:
        await asyncio.to_thread(run_alembic_migrations)
        logger.info("Alembic migrations verified/applied successfully.")
    except Exception as exc:
        logger.warning("Alembic migration check encountered an issue: %s", exc)

    return await seed_database_if_empty()
