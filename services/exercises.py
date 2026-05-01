from repositories.crud import CRUDBase
from models.models import Exercise, RoutineDay, ExerciseDetail
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm
from typing import Optional
from schemas.exercises import ExerciseDetailsUpdate


class ExerciseService:
    def __init__(self):
        self.crud_exercise = CRUDBase(Exercise)
        self.crud_details = CRUDBase(ExerciseDetail)
        self.crud_day = CRUDBase(RoutineDay)
    
    def get_all(self, limit: int = 6, category: str = "", name : str = ""):
        """Get exercises with optional category filter"""
        with database.session as sess:
            query = sqlm.select(Exercise)
            if category:
                query = query.where(Exercise.muscles.contains(category))
            elif name:
                query = query.where(Exercise.exercise_name.contains(name))
            exercises = sess.exec(query.limit(limit)).all()
            return exercises
    
    def add_detail(self, exercise_id: int, data):
        """Add exercise details to a day"""
        with database.session as sess:
            exercise = sess.exec(sqlm.select(Exercise).where(Exercise.id == exercise_id)).first()
            if not exercise:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
        
        detail_data = {
            "exersise_id": exercise_id,
            "name": exercise.exersise_name,
            "equipment_needed": exercise.equipment_needed,
            **data.dict()
        }
        return self.crud_details.create(detail_data)
    
    def get_by_day(self, day_id: int):
        """Get all exercise details for a specific day"""
        with database.session as sess:
            day = sess.exec(sqlm.select(RoutineDay).where(RoutineDay.id == day_id)).first()
            if not day:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
            return day.exercises if hasattr(day, 'exercises') else []
        
    def update_detail(self, detail_id : int, data : ExerciseDetailsUpdate):
        """Update Exercise details"""
        with database.session as sess:
            detail = sess.exec(sqlm.select(ExerciseDetail).where(ExerciseDetail.id==detail_id))
            if not detail:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")
            return self.crud_details.update(detail_id, data)
            
                
