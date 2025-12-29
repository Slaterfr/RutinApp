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

class DaysRead(SQLModel):
    owner_id : int
    name : str
    days_trained : int
    days : list
    
class DayUpdate(SQLModel):
    day_number : Optional[int]
    day_name : Optional[str]
    focus_area : Optional[str]

class ExerciseDetailsCreate(SQLModel):
    day_id : int
    set_count : int
    rep_target : int
    rest_seconds : int
    weight_notes : str

class UserCreate(SQLModel):
    username : str
    bio : Optional[str]
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

