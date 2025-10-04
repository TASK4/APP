from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.utils.auth import create_jwt_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

users_db = {}  # Demo giả lập database

@router.post("/register")
def register(user: UserCreate):
    if user.username in users_db:
        return {"error": "User already exists"}
    users_db[user.username] = hash_password(user.password)
    return {"msg": "User created"}

@router.post("/login")
def login(user: UserLogin):
    if user.username not in users_db or not verify_password(user.password, users_db[user.username]):
        return {"error": "Invalid credentials"}
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token}
