from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
# schemas define the structure of a request & response
# help with validation


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    # convert sqlalchemy model to pydantic model
    class Config:
        orm_mode = True


class Post(BaseModel):  # Post class model for post
    title: str
    content: str
    published: bool = False  # False by default


class PostResponse(Post):
    created_at: datetime
    user_id: int
    user: UserResponse

    # convert sqlalchemy model to pydantic model
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenRequest(BaseModel):
    id: Optional[str] = None
