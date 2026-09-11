# Database Schema Foundation & Domain Roadmap

This directory contains pure SQL DDL definitions and domain architecture blueprints for the Restaurant Platform.

## 1. Implemented Core Schema (Foundation)
The core tables provide the immediate foundation for tenant, menu, and user management:
- `users`: Accounts for customers, staff, managers, and system administrators.
- `restaurants`: Multi-tenant restaurant entity.
- `restaurant_branches`: Physical locations/branches with geographic coordinates.
- `menus`: Digital menus tied to restaurants.
- `menu_categories`: Sections grouping dishes within a menu (e.g., Starters, Mains, Desserts).
- `menu_items`: Individual dishes and products with exact `NUMERIC(10, 2)` monetary values.

## 2. Planned Domain Schema Catalog

The following domain tables are established in the architecture for upcoming development phases:

### User & Health Profiles
- `customer_profiles`: Extended preferences, avatars, and loyalty points.
- `addresses`: Delivery and billing locations with coordinates.
- `dietary_preferences`: System-wide dietary catalog (Vegan, Keto, Halal, Kosher).
- `user_dietary_preferences`: Many-to-many user preferences mapping.
- `allergens`: Common allergen definitions (Peanuts, Gluten, Dairy, Shellfish).
- `user_allergies`: Many-to-many user allergy mapping.
- `nutrition_goals`: Target macros and daily calorie objectives.
- `user_nutrition_profiles`: Macro ratios and active health goals.

### Nutritional & Ingestion Pipeline
- `ingredients`: Recipe ingredients and sourcing metadata.
- `menu_item_ingredients`: Many-to-many ingredients per menu item.
- `menu_item_allergens`: Allergen warnings per dish.
- `nutrition_facts`: Protein, carbohydrates, fats, sodium, and micronutrient breakdowns.
- `menu_scans`: OCR/AI ingestion staging records for scanned paper/PDF menus.

### Dining, QR & Reservations
- `restaurant_tables`: Physical floor tables with capacities and seat numbers.
- `qr_codes`: Table-specific or takeaway QR identifiers and scan links.
- `reservation_slots`: Time slot availability rules and capacity limits.
- `reservations`: Table bookings and guest requests.

### Ordering & Transactions
- `carts`: Persistent shopping carts across sessions and devices.
- `cart_items`: Selected items, customizations, and special requests.
- `orders`: Confirmed customer orders with kitchen status lifecycle.
- `order_items`: Order line items with historical price snapshots.
- `payments`: Stripe payment intents and transaction logs.
- `refunds`: Partial and full refund audit entries.

### Personalization & Engagement
- `food_logs`: Calorie and nutritional consumption tracking.
- `favorites_restaurants`: User saved restaurants.
- `favorites_menu_items`: User bookmarked dishes.
- `reviews`: Star ratings and verified customer reviews.
- `offers`: Promotional discount codes and marketing campaigns.
- `user_devices`: Push notification tokens (FCM/APNs) for mobile devices.
- `notifications`: In-app notification inbox.
- `audit_logs`: Security and administrative action audit trail.
