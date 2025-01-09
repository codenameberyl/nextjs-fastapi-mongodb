from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str
    password: str
    created_at: datetime
    last_login: Optional[datetime] = None