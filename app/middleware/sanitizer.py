from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.sanitization import sanitize_input
import bleach
import json

class SanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # --- 1️⃣ Làm sạch query params ---
        query_params = dict(request.query_params)
        for key, value in query_params.items():
            query_params[key] = bleach.clean(value, tags=[], strip=True)

        # --- 2️⃣ Làm sạch body JSON (nếu có) ---
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.json()
                # Dùng sanitize_input nếu là dict, fallback sang bleach nếu lỗi
                if isinstance(body, dict):
                    sanitized_body = sanitize_input(body)
                else:
                    sanitized_body = bleach.clean(str(body), tags=[], strip=True)
                
                # Override lại request body
                request._body = json.dumps(sanitized_body).encode("utf-8")
            except Exception:
                # Không có body JSON hoặc lỗi parse → bỏ qua
                pass

        # --- 3️⃣ Gọi tiếp middleware chain ---
        response = await call_next(request)
        return response
