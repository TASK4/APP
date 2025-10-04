from fastapi import FastAPI
from .routers import auth_router  # nếu bạn có router auth
from middleware import sanitizer, rate_limiter  # nếu bạn đã viết middleware

# Khởi tạo FastAPI app
app = FastAPI(
    title="Data Sanitization API",
    description="API demo với middleware làm sạch dữ liệu và giới hạn request",
    version="1.0.0",
)

# Gắn middleware vào app
# (tùy bạn đã viết sanitizer.py và rate_limiter.py thế nào, ví dụ mình giả sử có dạng add_middleware)
# app.add_middleware(sanitizer.SanitizerMiddleware)
# app.add_middleware(rate_limiter.RateLimiterMiddleware)

# Include router
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

# Root endpoint test
@app.get("/")
async def root():
    return {"message": "Hello, API is running!"}
