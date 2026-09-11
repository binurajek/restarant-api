-- ==============================================================================
-- Core Schema DDL Reference (PostgreSQL 16+ / Neon)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(128) NOT NULL,
    phone VARCHAR(32),
    role VARCHAR(32) NOT NULL DEFAULT 'customer',
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users(email);
CREATE INDEX IF NOT EXISTS ix_users_id ON users(id);

-- 2. Restaurants
CREATE TABLE IF NOT EXISTS restaurants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    slug VARCHAR(128) NOT NULL,
    description TEXT,
    logo_url VARCHAR(512),
    cover_image_url VARCHAR(512),
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    is_active BOOLEAN NOT NULL DEFAULT true,
    owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_restaurants_slug ON restaurants(slug);
CREATE INDEX IF NOT EXISTS ix_restaurants_id ON restaurants(id);
CREATE INDEX IF NOT EXISTS ix_restaurants_name ON restaurants(name);
CREATE INDEX IF NOT EXISTS ix_restaurants_owner_id ON restaurants(owner_id);

-- 3. Restaurant Branches
CREATE TABLE IF NOT EXISTS restaurant_branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    address_line VARCHAR(255) NOT NULL,
    city VARCHAR(64) NOT NULL,
    state_or_province VARCHAR(64),
    postal_code VARCHAR(32),
    country_code VARCHAR(2) NOT NULL DEFAULT 'US',
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    phone VARCHAR(32),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_restaurant_branches_id ON restaurant_branches(id);
CREATE INDEX IF NOT EXISTS ix_restaurant_branches_restaurant_id ON restaurant_branches(restaurant_id);
CREATE INDEX IF NOT EXISTS ix_restaurant_branches_city ON restaurant_branches(city);

-- 4. Menus
CREATE TABLE IF NOT EXISTS menus (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_menus_id ON menus(id);
CREATE INDEX IF NOT EXISTS ix_menus_restaurant_id ON menus(restaurant_id);

-- 5. Menu Categories
CREATE TABLE IF NOT EXISTS menu_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_id UUID NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    name VARCHAR(64) NOT NULL,
    description VARCHAR(255),
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_menu_categories_id ON menu_categories(id);
CREATE INDEX IF NOT EXISTS ix_menu_categories_menu_id ON menu_categories(menu_id);

-- 6. Menu Items
CREATE TABLE IF NOT EXISTS menu_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID NOT NULL REFERENCES menu_categories(id) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    image_url VARCHAR(512),
    is_available BOOLEAN NOT NULL DEFAULT true,
    calories INT,
    preparation_time_minutes INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_menu_items_id ON menu_items(id);
CREATE INDEX IF NOT EXISTS ix_menu_items_category_id ON menu_items(category_id);
CREATE INDEX IF NOT EXISTS ix_menu_items_name ON menu_items(name);
