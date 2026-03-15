from typing import Optional
from pydantic import BaseModel

# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str

# Properties to return via API
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
