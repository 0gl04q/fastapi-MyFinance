from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    is_active: bool


class User(UserBase, UserUpdate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
