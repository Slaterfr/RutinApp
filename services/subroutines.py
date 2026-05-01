from repositories.crud import CRUDBase
from models.models import Routine, RoutineDay
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm


class SubRoutineService:
    def __init__(self):
        self.crud_routine = CRUDBase(Routine)
        self.crud_day = CRUDBase(RoutineDay)
    
    def get_days(self, routine_id: int):
        """Get all days for a routine"""
        with database.session as sess:
            routine = sess.exec(sqlm.select(Routine).where(Routine.id == routine_id)).first()
            if not routine:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
            return routine.days if hasattr(routine, 'days') else []
    
    def create_day(self, routine_id: int, data, user_id: int):
        """Create a new day in a routine (ownership check)"""
        routine = self.crud_routine.read(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        if routine.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this routine")
        
        day_data = {**data.dict(), "routine_id": routine_id}
        return self.crud_day.create(day_data)
    
    def update_day(self, routine_id: int, day_id: int, data, user_id: int):
        """Update a day (ownership check)"""
        routine = self.crud_routine.read(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        if routine.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this routine")
        
        day = self.crud_day.read(day_id)
        if not day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
        
        return self.crud_day.update(day_id, data.dict())
    
    def delete_day(self, routine_id: int, day_id: int, user_id: int):
        """Delete a day (ownership check)"""
        routine = self.crud_routine.read(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        if routine.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this routine")
        
        day = self.crud_day.read(day_id)
        if not day:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
        
        success = self.crud_day.delete(day_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete day")
        
        return {"message": "Day deleted successfully"}
