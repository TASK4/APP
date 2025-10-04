from fastapi import FastAPI
from app.middleware.santinizer import SanitizerMiddleware
from app.routers import auth_router

app = FastAPI()

app.add_middleware(SanitizerMiddleware)

app.include_router(auth_router.router)
