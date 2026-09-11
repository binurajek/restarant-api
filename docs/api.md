# API Specification and Routing

The platform exposes a centralized REST API versioned under `/api/v1`.

## 1. Base URL & Documentation
- **API Base Path**: `/api/v1`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc UI**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## 2. Core Endpoints Summary

### Health & Observability
| Method | Endpoint | Description | Response |
|---|---|---|---|
| `GET` | `/api/v1/health` | Liveness check | `{"status": "ok"}` |
| `GET` | `/api/v1/health/database` | Database connectivity & latency | `{"status": "ok", "database": "connected", "latency_ms": 1.2}` |

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user account |
| `POST` | `/api/v1/auth/login` | Login and receive Access & Refresh JWT tokens |

### Users
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users/{user_id}` | Fetch user profile |
| `PATCH` | `/api/v1/users/{user_id}` | Update user profile |

### Restaurants
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/restaurants` | Create restaurant entity |
| `GET` | `/api/v1/restaurants` | List restaurants (paginated) |
| `GET` | `/api/v1/restaurants/{restaurant_id}` | Get restaurant with branches |
| `GET` | `/api/v1/restaurants/by-slug/{slug}` | Get restaurant by unique slug |
| `PATCH` | `/api/v1/restaurants/{restaurant_id}` | Update restaurant profile |

### Menus & Categories
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/menus` | Create digital menu |
| `GET` | `/api/v1/menus/{menu_id}` | Get menu with categories and dishes |
| `GET` | `/api/v1/menus/restaurant/{restaurant_id}` | List menus for a restaurant |
| `PATCH` | `/api/v1/menus/{menu_id}` | Update menu details |
| `POST` | `/api/v1/menu-items` | Add item to menu category |
| `GET` | `/api/v1/menu-items/{item_id}` | Get dish item details |
| `PATCH` | `/api/v1/menu-items/{item_id}` | Update dish item details |

---

## 3. Standard Response Formats

### Pagination Response Container
```json
{
  "items": [],
  "total": 120,
  "page": 1,
  "page_size": 20,
  "total_pages": 6
}
```

### Error Response Schema
```json
{
  "error": {
    "code": 404,
    "message": "Restaurant not found.",
    "request_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
}
```
