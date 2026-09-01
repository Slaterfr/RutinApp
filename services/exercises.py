from repositories.crud import CRUDBase
from models.models import Exercise, RoutineDay, ExerciseDetail
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm
from typing import Optional
from schemas.exercises import ExerciseDetailsUpdate
from services.redis.caching import RedisService

import json
import time 
from .logging.loggerservice import logger
from .redis.redisconfig import redis_client

class ExerciseService:
    def __init__(self):
        self.crud_exercise = CRUDBase(Exercise)
        self.crud_details = CRUDBase(ExerciseDetail)
        self.crud_day = CRUDBase(RoutineDay)
        self.ttl = 300
    async def get_all(self, limit: int = 6, category: str = "", name : str = ""):
        """Get exercises with optional category filter"""
        key = f"exercises:{category}"
        async def fetch():
            with database.session as sess:
                
                query = sqlm.select(Exercise)
                if name:
                    query = query.where(Exercise.exercise_name.ilike(f"%{name}%"))
                if category:
                    # Filter by muscle - muscles are stored as comma-separated text
                    query = query.where(Exercise.muscles.ilike(f"%{category}%"))
                
                exercises = sess.exec(query.limit(limit)).all()

                serialized_exercises = [
                    exercise.model_dump()
                    for exercise in exercises
                ]
                return serialized_exercises
        if name:        
            return await fetch()
        try:
            return await RedisService.caching_aside(self, key, fetch)
        except Exception as e:
            logger.error(f"Error al obtener ejercicios: {e}")
            return await fetch()
        
    async def get_by_id(self, exercise_id):
        """Get a specific exercise by ID"""
        with database.session as sess:
            
            query = sqlm.select(Exercise).where(Exercise.id == exercise_id)
            exercise = sess.exec(query).one()
           
            return exercise.model_dump()
    
    def add_detail(self, exercise_id: int, data):
        """Add exercise details to a day"""
        with database.session as sess:
            exercise = sess.exec(sqlm.select(Exercise).where(Exercise.id == exercise_id)).first()
            if not exercise:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
        
        detail_data = {
            "exercise_id": exercise_id,
            "name": exercise.exercise_name,
            "equipment_needed": exercise.equipment_needed,
            **data.dict()
        }
        
        sess.add(ExerciseDetail(**detail_data))
        sess.commit()
        return detail_data
    
    def get_by_day(self, day_id: int):
        """Get all exercise details for a specific day"""
        with database.session as sess:
            day = sess.exec(sqlm.select(RoutineDay).where(RoutineDay.id == day_id)).first()
            if not day:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
            
            query = (
                sqlm.select(ExerciseDetail, Exercise)
                .join(Exercise, ExerciseDetail.exercise_id == Exercise.id)
                .where(ExerciseDetail.day_id == day_id)
            )
            results = sess.exec(query).all()
            
            return [
                {
                    "id": detail.id,
                    "exercise_detail_id": detail.id,
                    "exercise_id": detail.exercise_id,
                    "day_id": detail.day_id,
                    "set_count": detail.set_count,
                    "rep_target": detail.rep_target,
                    "rest_seconds": detail.rest_seconds,
                    "weight_notes": detail.weight_notes,
                    "exercise_name": exercise.exercise_name,
                    "name": exercise.exercise_name,
                    "category": exercise.category,
                    "equipment": exercise.equipment_needed,
                    "muscles": exercise.muscles,
                }
                for detail, exercise in results
            ]
        
    def update_detail(self, detail_id : int, data : ExerciseDetailsUpdate):
        """Update Exercise details"""
        with database.session as sess:
            detail = sess.exec(sqlm.select(ExerciseDetail).where(ExerciseDetail.id==detail_id))
            if not detail:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")
            return self.crud_details.update(detail_id, data)
            
                
