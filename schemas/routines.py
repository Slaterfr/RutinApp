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