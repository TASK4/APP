from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # type: ignore
    password: constr(min_length=6)  # type: ignore

class UserLogin(BaseModel):
    username: str
    password: str