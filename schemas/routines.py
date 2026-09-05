from pydantic import BaseModel, Field, field_validator
from typing import Optional
from sqlmodel import SQLModel


class DayInfo(BaseModel):
    id: int
    day_number: int
    day_name: str
    focus_area: str
    weekday: Optional[int] = None


class Routine(SQLModel):
    name: str = Field(..., min_length=1, max_length=100, description="Routine name")
    days_per_week: int = Field(..., gt=0, le=7, description="Days per week (1-7)")
    estimated_hours: float = Field(..., gt=0, le=24, description="Hours per week (0-24)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Routine name cannot be empty or whitespace only')
        return v.strip()


class RoutinesRead(BaseModel):
    owner_id: int
    id: int
    name: str
    days_per_week: int
    estimated_hours: float


class RoutineRead(BaseModel):
    id: int
    name: str
    days_per_week: int
    estimated_hours: float
    days: list[DayInfo]


class RoutineUpdate(SQLModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    days_per_week: Optional[int] = Field(None, gt=0, le=7)
    estimated_hours: Optional[float] = Field(None, gt=0, le=24)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Routine name cannot be empty or whitespace only')
        return v.strip() if v else None


class RoutineSearch(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)