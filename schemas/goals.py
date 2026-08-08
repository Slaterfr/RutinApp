from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import SQLModel
from datetime import date
from pydantic import Field

class GoalCreate(BaseModel):
    current_weight: float = Field(..., ge=30, description="Weight in Kilograms")
    goal_weight: float = Field(..., gt=current_weight, description="Goal Weight in Kilograms")
    current_physique_id: int 
    goal_physique_id: int 
    priority: int # 1 = highest, 2 = medium, 3 = lowest
    notes: Optional[str] = None
    achieved_at: Optional[date] = None


class GoalRead(BaseModel):
    current_weight: float 
    goal_weight: float 
    current_physique_id: int 
    goal_physique_id: int 
    priority: int # 1 = highest, 2 = medium, 3 = lowest
    notes: Optional[str] = None
    achieved_at: Optional[date] = None

class GoalUpdate(BaseModel):
    current_weight: Optional[float] 
    goal_weight: Optional[float] 
    current_physique_id: Optional[int] 
    goal_physique_id: Optional[int] 
    priority: Optional[int ]# 1 = highest, 2 = medium, 3 = lowest
    notes: Optional[str] = None
    achieved_at: Optional[date] = None

    