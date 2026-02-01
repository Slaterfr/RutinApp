from ...db import database
from ...models import models
from ...schemas import DayCreate, DayUpdate
from ...dependencys import utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from sqlmodel import join




router = APIRouter(
    prefix='/routines',
    tags=['subroutines']
)

@router.get('/{id}/days')
def get_days(id : int):
    with database.session as sess:
        currentRoutine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        return currentRoutine, currentRoutine.days


@router.post('/{id}/days')
def post_day(data : DayCreate, id : int, user_id: int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        currentRoutine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        if user_id.id !=currentRoutine.owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        
        new_day = models.DiaRutina(routine_id=currentRoutine.id, **data.dict())
        sess.add(new_day)
        sess.commit()
    return new_day


@router.put('/{id}/days/{day_id}')
def update_day(data : DayUpdate, id: int, day_id : int, user_id: int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        currentRoutine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        if currentRoutine.owner_id != user_id.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        currentRoutine.sqlmodel_update(data)
        sess.add(currentRoutine)
        sess.commit()
        

@router.delete('/{id}/days/{day_id}')
def delete_day(id : int, day_id : int, user_id : int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        currentRoutine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        if currentRoutine.owner_id != user_id.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        day = sess.exec(sqlm.select(models.DiaRutina).where(models.DiaRutina.id == day_id)).one()

        sess.delete(day)
        sess.commit()

        return {"Day deleted"}
