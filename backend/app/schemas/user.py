from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100, example="yourpassword123")
    confirm_password: str = Field(..., min_length=8, max_length=100, example="yourpassword123")

    @model_validator(mode="after")
    def passwords_match(cls, values: "UserCreate") -> "UserCreate":
        if values.password != values.confirm_password:
            raise ValueError("Passwords do not match")
        return values


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    profile_bio: Optional[str] = Field(None, max_length=500)


class UserInDB(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    password: str
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    profile_bio: Optional[str] = Field(None, max_length=500)
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False


class UserResponse(UserBase):
    id: str
    created_at: datetime
    last_login: Optional[datetime]
    is_verified: bool

    class Config:
        from_attributes = True
