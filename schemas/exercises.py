from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel


class ExerciseDetailsCreate(SQLModel):
    day_id : int
    set_count : int
    rep_target : int
    rest_seconds : int
    weight_notes : str

class ExerciseDetailsUpdate(SQLModel):
    set_count : Optional[int]
    rep_target : Optional[int]
    rest_seconds : Optional[int]
    weight_notes : Optional[str]