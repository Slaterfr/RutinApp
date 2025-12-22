from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel

class Routine(SQLModel):
    name : str 
    days_trained : int
    hours_trained : float

class RoutinesRead(BaseModel):
    owner_id : int
    id : int
    name : str
    days_trained : int
    hours_trained : float

class RoutineRead(BaseModel):
    id : int
    name : str
    days_trained : int
    hours_trained : float
    days : list

class RoutineUpdate(SQLModel):
    name : Optional[str]
    days_trained : Optional[int]
    hours_trained : Optional[float]

class RoutineSearch(BaseModel):
    name : str

class DayCreate(SQLModel):
    day_number : int
    day_name : str
    focus_area : str
    

class UserCreate(SQLModel):
    email : EmailStr
    password : str

class UserResponse(SQLModel):
    email : EmailStr

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] 


class BotRequest(BaseModel):
    User_input : str

