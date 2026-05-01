from repositories.crud import CRUDBase
from services.handlers import InvalidData
from models.models import Session, Routine, RoutineDay
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm
from typing import Optional
from datetime import date


class SessionService:
    def __init__(self):
        self.crud = CRUDBase(Session)
    
    def create(self, data, user_id: int):
        """Create a new workout session"""
        # Validate routine exists and belongs to user
        with database.session as sess:
            routine = sess.exec(sqlm.select(Routine).where(Routine.id == data.routine_id)).first()
            if not routine:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
            if routine.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to use this routine")
            
            # Validate day exists and belongs to routine
            day = sess.exec(sqlm.select(RoutineDay).where(RoutineDay.id == data.day_id)).first()
            if not day:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training day not found")
            if day.routine_id != data.routine_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Day does not belong to this routine")
        
        session_data = {**data.model_dump(), "user_id": user_id}
        return self.crud.create(session_data)
    
    def get_by_id(self, session_id: int):
        """Get a specific session by ID"""
        session = self.crud.read(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return session
    
    def get_user_sessions(self, user_id: int, skip: int = 0, limit: int = 10, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get all sessions for a user with optional date filtering"""
        with database.session as sess:
            query = sqlm.select(Session).where(Session.user_id == user_id)
            
            if start_date:
                query = query.where(Session.session_date >= start_date)
            if end_date:
                query = query.where(Session.session_date <= end_date)
            
            sessions = sess.exec(query.offset(skip).limit(limit)).all()
            return sessions
    
    def update(self, session_id: int, data, user_id: int):
        """Update a session (ownership check)"""
        session = self.crud.read(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        if session.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this session")
        
        return self.crud.update(session_id, data.model_dump(exclude_unset=True))
    
    def delete(self, session_id: int, user_id: int):
        """Delete a session (ownership check)"""
        session = self.crud.read(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        if session.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this session")
        
        self.crud.delete(session_id)
        return {"message": "Session deleted successfully"}
