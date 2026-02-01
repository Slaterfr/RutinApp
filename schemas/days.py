from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel


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