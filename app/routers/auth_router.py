# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils.logging import logger
from ..utils.security import get_password_hash, verify_password
from ..utils.auth import create_access_token, get_current_user, oauth2_scheme

router = APIRouter()

# --- Đăng ký tài khoản ---
@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Dùng user.username làm email để lưu vào DB
    email_to_register = user.username
    logger.info(f"Attempting to register new user: {email_to_register}")
    
    db_user = db.query(models.User).filter(models.User.email == email_to_register).first()
    if db_user:
        logger.warning(f"Registration failed: Username {email_to_register} already registered.")
        raise HTTPException(status_code=400, detail="Username already registered")
    
    default_role = db.query(models.Role).filter(models.Role.name == "user").first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Default user role not found.")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        email=email_to_register, 
        hashed_password=hashed_password, 
        role_id=default_role.id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User {email_to_register} created successfully with ID {new_user.id}.")
    return new_user

# --- Đăng nhập ---
@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Dùng OAuth2PasswordRequestForm (Swagger sẽ tự hiện form username/password)
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"User {form_data.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}

# --- Lấy thông tin người dùng hiện tại ---
@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Get current logged in user's information.
    """
    return current_user
