from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.sanitization import sanitize_input

class SanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.json()
            cleaned_body = {k: sanitize_input(v) for k, v in body.items()}
            request._body = str(cleaned_body).encode()
        response = await call_next(request)
        return response
