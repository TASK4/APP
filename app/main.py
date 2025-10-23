from fastapi import FastAPI, Request
from .database import Base, engine, SessionLocal
from .routers import auth_router
from .utils.logging import logger
from . import models
from fastapi.responses import JSONResponse
import traceback # Import traceback

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Demo API",
    description="API for user registration demo.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup.")
    db = SessionLocal()
    try:
        # Create a default role if it doesn't exist
        default_role = db.query(models.Role).filter(models.Role.name == "user").first()
        if not default_role:
            db_role = models.Role(name="user")
            db.add(db_role)
            db.commit()
            logger.info("Default role 'user' created.")
    finally:
        db.close()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Response: status_code={response.status_code}")
        return response
    except Exception as e:
        # Sửa lại cách gọi hàm này cho đúng
        tb_str = traceback.format_exception(e)
        logger.error("".join(tb_str))
        # Trả về lỗi 500 chung chung cho client
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API is running!"}