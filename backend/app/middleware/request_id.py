"""Request ID / Correlation ID Middleware."""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import correlation_id_ctx

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assigns or propagates a unique correlation ID per request."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        req_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        token = correlation_id_ctx.set(req_id)
        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = req_id
            return response
        finally:
            correlation_id_ctx.reset(token)
