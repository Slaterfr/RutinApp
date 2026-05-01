from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 chars)")
    bio: Optional[str] = Field(None, max_length=500, description="User bio")
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @field_validator('username', 'bio')
    @classmethod
    def validate_strings(cls, v, info):
        if v and isinstance(v, str) and not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip() if v else None


class UserResponse(SQLModel):
    email: EmailStr


class UserInfo(SQLModel):
    email: EmailStr
    username: str
    biography: Optional[str]



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Optional[int]


class BotRequest(BaseModel):
    User_input: str = Field(..., min_length=1, max_length=5000, description="User message")

    @field_validator('User_input')
    @classmethod
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1, description="Valid refresh token")