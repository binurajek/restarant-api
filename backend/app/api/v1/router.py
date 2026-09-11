"""Central API v1 Router Aggregator."""

from fastapi import APIRouter

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.menu_items import router as menu_items_router
from app.api.v1.menus import router as menus_router
from app.api.v1.orders import router as orders_router
from app.api.v1.reservations import router as reservations_router
from app.api.v1.restaurants import router as restaurants_router
from app.api.v1.users import router as users_router

api_v1_router = APIRouter()

# Register core active modules
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(restaurants_router)
api_v1_router.include_router(menus_router)
api_v1_router.include_router(menu_items_router)

# Register future domain placeholders
api_v1_router.include_router(orders_router)
api_v1_router.include_router(reservations_router)
api_v1_router.include_router(admin_router)
