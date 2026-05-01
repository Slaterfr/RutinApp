from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel


class WorkoutSetCreate(SQLModel):
    exercise_detail_id: int = Field(..., gt=0, description="Exercise detail ID")
    set_number: int = Field(..., gt=0, le=100, description="Set number (1-100)")
    reps: int = Field(..., gt=0, le=500, description="Reps completed (1-500)")
    weight: float = Field(..., ge=0, le=1000, description="Weight used (0-1000)")
    notes: Optional[str] = Field(None, max_length=500, description="Performance notes")

    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class WorkoutSetUpdate(SQLModel):
    set_number: Optional[int] = Field(None, gt=0, le=100)
    reps: Optional[int] = Field(None, gt=0, le=500)
    weight: Optional[float] = Field(None, ge=0, le=1000)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class WorkoutSetRead(BaseModel):
    id: int
    session_id: int
    exercise_detail_id: int
    set_number: int
    reps: int
    weight: float
    notes: Optional[str]

    class Config:
        from_attributes = True
