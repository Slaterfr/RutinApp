from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel


class DayCreate(SQLModel):
    day_number: int = Field(..., ge=1, le=7, description="Day number (1-7)")
    day_name: str = Field(..., min_length=1, max_length=50, description="Day name (e.g., Push, Pull, Legs)")
    focus_area: str = Field(..., min_length=1, max_length=100, description="Focus area/muscle groups")

    @field_validator('day_name', 'focus_area')
    @classmethod
    def validate_strings(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()


class DaysRead(SQLModel):
    owner_id: int
    name: str
    days_trained: int
    days: list


class DayUpdate(SQLModel):
    day_number: Optional[int] = Field(None, ge=1, le=7)
    day_name: Optional[str] = Field(None, min_length=1, max_length=50)
    focus_area: Optional[str] = Field(None, min_length=1, max_length=100)

    @field_validator('day_name', 'focus_area')
    @classmethod
    def validate_strings(cls, v):
        if v and not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip() if v else None