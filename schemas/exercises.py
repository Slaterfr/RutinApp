from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel


class ExerciseDetailsCreate(SQLModel):
    day_id : int
    set_count : int
    rep_target : int
    rest_seconds : int
    weight_notes : str