from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

# --- Schema đăng nhập ---
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    # Thêm schema mới cho việc đăng nhập
    username: str
    password: str


# --- Schema cập nhật user ---
class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None


# --- Schema đổi mật khẩu ---
class ChangePasswordSchema(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

# --- Schema phản hồi (trả về client) ---
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int

    class Config:
        orm_mode = True

# Schema for creating a user (input)
class UserCreate(BaseModel):
    username: str
    password: str

# Schema for reading a user (output)
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None