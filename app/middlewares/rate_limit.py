import time
from typing import Callable, Dict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.config import settings
from app.core.exceptions import RateLimitExceededError


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.rate_limits: Dict[str, Dict] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"

        current_time = time.time()
        if client_ip in self.rate_limits:
            rate_limit_info = self.rate_limits[client_ip]

            if (
                current_time - rate_limit_info["start_time"]
                > settings.RATE_LIMIT_DEFAULT_PERIOD
            ):
                rate_limit_info["count"] = 1
                rate_limit_info["start_time"] = current_time
            else:
                rate_limit_info["count"] += 1

                if rate_limit_info["count"] > settings.RATE_LIMIT_DEFAULT_LIMIT:
                    raise RateLimitExceededError()
        else:
            self.rate_limits[client_ip] = {"count": 1, "start_time": current_time}
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_DEFAULT_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(
            max(
                0,
                settings.RATE_LIMIT_DEFAULT_LIMIT
                - self.rate_limits[client_ip]["count"],
            )
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(
                self.rate_limits[client_ip]["start_time"]
                + settings.RATE_LIMIT_DEFAULT_PERIOD
            )
        )

        return response