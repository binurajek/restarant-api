"""Application Constants and Enumerations."""

from enum import StrEnum


class Environment(StrEnum):
    """Application runtime environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class UserRole(StrEnum):
    """User authorization roles."""

    CUSTOMER = "customer"
    RESTAURANT_STAFF = "restaurant_staff"
    RESTAURANT_MANAGER = "restaurant_manager"
    RESTAURANT_OWNER = "restaurant_owner"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(StrEnum):
    """User account statuses."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class RestaurantStatus(StrEnum):
    """Restaurant lifecycle statuses."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class MenuStatus(StrEnum):
    """Menu lifecycle statuses."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class OrderStatus(StrEnum):
    """Customer order statuses."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(StrEnum):
    """Transaction payment statuses."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class ReservationStatus(StrEnum):
    """Table reservation statuses."""

    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
