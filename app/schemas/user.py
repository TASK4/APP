# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

# --- Schema đăng nhập ---
class LoginSchema(BaseModel):
    # Sửa lại: Chỉ cần username và password
    username: str
    password: str
    # Xóa các trường bị trùng lặp


# --- Schema cập nhật user ---
class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    role_id: Optional[int] = None


# --- Schema đổi mật khẩu ---
class ChangePasswordSchema(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

# --- Schema phản hồi (trả về client) ---
class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):

    username: str
    password: str

class User(BaseModel):
    id: int
    username: str 

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None