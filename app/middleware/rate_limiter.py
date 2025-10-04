from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time

requests = {}

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        now = time.time()
        window = 60  # 1 phút
        limit = 30   # tối đa 30 request

        if ip not in requests:
            requests[ip] = []
        requests[ip] = [t for t in requests[ip] if now - t < window]

        if len(requests[ip]) >= limit:
            return JSONResponse({"detail": "Too many requests"}, status_code=429)

        requests[ip].append(now)
        response = await call_next(request)
        return response
