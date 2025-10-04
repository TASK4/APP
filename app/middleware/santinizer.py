from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.sanitization import sanitize_input

class SanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.json()
            sanitized_body = sanitize_input(body)
            request._body = sanitized_body
        response = await call_next(request)
        return response