"""Structured HTTP Request Logging Middleware."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger("http.access")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests and response performance metrics."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        method = request.method
        url = request.url.path

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                "%s %s completed in %sms with status %s",
                method,
                url,
                duration_ms,
                response.status_code,
            )
            return response
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                "%s %s failed in %sms: %s",
                method,
                url,
                duration_ms,
                str(exc),
                exc_info=True,
            )
            raise
