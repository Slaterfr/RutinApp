from pydantic import BaseModel
from datetime import date
from typing import Dict


class DashboardStatsRead(BaseModel):
    total_workouts: int
    total_volume: float
    muscle_distribution: Dict[str, int]
    active_streak: int


class HistoricalStatsRead(BaseModel):
    week_start_date: date
    workouts_completed: int
    total_volume: float
    total_sets: int

    class Config:
        from_attributes = True
