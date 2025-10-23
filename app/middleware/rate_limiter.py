from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from collections import defaultdict
import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 60, window: int = 60):
        """
        Middleware giới hạn tần suất request theo IP.
        :param limit: Số lượng request tối đa trong khoảng thời gian `window`.
        :param window: Khoảng thời gian tính bằng giây (mặc định: 60s).
        """
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host or "unknown"
        current_time = time.time()

        # Dọn dẹp các timestamp cũ ngoài window
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if current_time - t < self.window
        ]

        # Check giới hạn request
        if len(self.requests[client_ip]) >= self.limit:
            reset_time = int(self.window - (current_time - self.requests[client_ip][0]))
            return JSONResponse(
                {
                    "detail": "Too many requests",
                    "retry_after": reset_time,
                    "limit": self.limit,
                    "window_seconds": self.window,
                },
                status_code=429,
                headers={"Retry-After": str(reset_time)},
            )

        # Ghi nhận thời điểm request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
