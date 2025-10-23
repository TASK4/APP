from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class SanitizationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def setup_exception_handlers(app):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(SanitizationError)
    async def sanitization_exception_handler(request: Request, exc: SanitizationError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )