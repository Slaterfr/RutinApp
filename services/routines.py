from repositories.crud import CRUDBase
from services.handlers import InvalidData
from models.models import Routine, RoutineDay
from db import database
from fastapi import HTTPException, status
import sqlmodel as sqlm


class RoutineService:
    def __init__(self):
        self.crud = CRUDBase(Routine)
    
    def create(self, data, user_id: int):
        """Validate and create a new routine"""
        if data.days_per_week < 1:
            raise InvalidData("Error, you routine can't have less than 1 day.")
        if data.days_per_week > 7:
            raise InvalidData("Error, you routine can't have more than 7 days. How many days does your week have?")
        
        routine_data = {**data.model_dump(), "owner_id": user_id}
        return self.crud.create(routine_data)
    
    def get_all(self, skip: int = 0, limit: int = 10, search: str = ""):
        """Get all routines with optional search filter"""
        routines = self.crud.read_all(skip=skip, limit=limit)
        if search:
            routines = [r for r in routines if search.lower() in r.name.lower()]
        return routines
    
    def get_user_routines(self, user_id : int):
        with database.session as sess:
            query = sqlm.select(Routine).where(Routine.owner_id == user_id)
            routines = sess.exec(query).all()
            return routines

    def get_by_id(self, routine_id: int):
        """Get a single routine by ID with its days"""
        with database.session as sess:
            routine = sess.exec(
                sqlm.select(Routine).where(Routine.id == routine_id)
            ).first()
            
            if not routine:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
            
            # Load days with the routine
            sess.refresh(routine)
            
            return routine
    
    def update(self, routine_id: int, data, user_id: int):
        """Update a routine (ownership check)"""
        routine = self.crud.read(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        if routine.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this routine")
        
        return self.crud.update(routine_id, data.dict())
    
    def delete(self, routine_id: int, user_id: int):
        """Delete a routine (ownership check)"""
        routine = self.crud.read(routine_id)
        if not routine:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Routine not found")
        if routine.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this routine")
        
        self.crud.delete(routine_id)
        return {"message": "Routine deleted successfully"}


