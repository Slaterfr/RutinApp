from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username : str
    bio : Optional[str]
    email : EmailStr
    password : str

class UserResponse(SQLModel):
    email : EmailStr

class UserInfo(SQLModel):
    email : EmailStr
    username : str
    biography : Optional[str]
    routines : list

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] 


class BotRequest(BaseModel):
    User_input : str

