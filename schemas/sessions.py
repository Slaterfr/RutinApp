from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel
from datetime import date


class SessionCreate(SQLModel):
    routine_id: int = Field(..., gt=0, description="Routine ID")
    day_id: int = Field(..., gt=0, description="Training day ID")
    session_date: date = Field(..., description="Date of the session")
    notes: Optional[str] = Field(None, max_length=1000, description="Session notes/observations")

    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class SessionUpdate(SQLModel):
    session_date: Optional[date] = Field(None, description="Date of the session")
    notes: Optional[str] = Field(None, max_length=1000, description="Session notes/observations")

    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v and not v.strip():
            return None
        return v.strip() if v else None


class SessionRead(BaseModel):
    id: int
    routine_id: int
    routine_name: Optional[str] = None
    day_id: int
    session_date: date
    notes: Optional[str]
    total_sets: int = 0

    class Config:
        from_attributes = True


class LastSession(SessionRead):
    day_name: str
    session_date : date
    