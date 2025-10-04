from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.utils.sanitization import sanitize_input

router = APIRouter()

@router.post("/login")
async def login_user(user: UserCreate):
    clean_data = sanitize_input(user.dict())
    return {"message": "User logged in", "data": clean_data}
