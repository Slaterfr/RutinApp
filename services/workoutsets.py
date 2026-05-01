from repositories.crud import CRUDBase
from services.handlers import InvalidData
from models.models import WorkoutSet, Session, ExerciseDetail
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm
from typing import Optional


class WorkoutSetService:
    def __init__(self):
        self.crud = CRUDBase(WorkoutSet)
    
    def create(self, session_id: int, data, user_id: int):
        """Create a new workout set for a session"""
        # Validate session exists and belongs to user
        with database.session as sess:
            session = sess.exec(sqlm.select(Session).where(Session.id == session_id)).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
            if session.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add sets to this session")
            
            # Validate exercise detail exists
            exercise_detail = sess.exec(sqlm.select(ExerciseDetail).where(ExerciseDetail.id == data.exercise_detail_id)).first()
            if not exercise_detail:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise detail not found")
        
        set_data = {**data.model_dump(), "session_id": session_id}
        return self.crud.create(set_data)
    
    def get_by_id(self, set_id: int):
        """Get a specific workout set by ID"""
        workout_set = self.crud.read(set_id)
        if not workout_set:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout set not found")
        return workout_set
    
    def get_session_sets(self, session_id: int):
        """Get all workout sets for a specific session"""
        with database.session as sess:
            session = sess.exec(sqlm.select(Session).where(Session.id == session_id)).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
            return session.sets if hasattr(session, 'sets') else []
    
    def update(self, set_id: int, data, user_id: int):
        """Update a workout set (ownership check via session)"""
        workout_set = self.crud.read(set_id)
        if not workout_set:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout set not found")
        
        # Verify session ownership
        with database.session as sess:
            session = sess.exec(sqlm.select(Session).where(Session.id == workout_set.session_id)).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
            if session.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this set")
        
        return self.crud.update(set_id, data.model_dump(exclude_unset=True))
    
    def delete(self, set_id: int, user_id: int):
        """Delete a workout set (ownership check via session)"""
        workout_set = self.crud.read(set_id)
        if not workout_set:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout set not found")
        
        # Verify session ownership
        with database.session as sess:
            session = sess.exec(sqlm.select(Session).where(Session.id == workout_set.session_id)).first()
            if not session:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
            if session.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this set")
        
        self.crud.delete(set_id)
        return {"message": "Workout set deleted successfully"}
