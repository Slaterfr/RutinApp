from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel


class ExerciseDetailsCreate(SQLModel):
    day_id: int = Field(..., gt=0, description="Training day ID")
    set_count: int = Field(..., gt=0, le=20, description="Number of sets (1-20)")
    rep_target: int = Field(..., gt=0, le=500, description="Target reps per set (1-500)")
    rest_seconds: int = Field(..., ge=0, le=600, description="Rest between sets in seconds (0-600)")
    weight_notes: Optional[str] = Field(None, max_length=500, description="Weight or notes")

    @field_validator('weight_notes')
    @classmethod
    def validate_weight_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class ExerciseDetailsUpdate(SQLModel):
    set_count: Optional[int] = Field(None, gt=0, le=20)
    rep_target: Optional[int] = Field(None, gt=0, le=500)
    rest_seconds: Optional[int] = Field(None, ge=0, le=600)
    weight_notes: Optional[str] = Field(None, max_length=500)

    @field_validator('weight_notes')
    @classmethod
    def validate_weight_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None
    

class ReadExercise(SQLModel):
    id: Optional[int] = None
    exercise_name: str
    instructions: str
    equipment_needed: Optional[str]
    category: str
    muscles : str
