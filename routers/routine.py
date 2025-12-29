from ..db import database, models
from .. import schemas, utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
import sqlalchemy
from typing import Optional



router = APIRouter(
    prefix='/routines',
    tags=['Routines']
)



@router.get('/', response_model=list[schemas.RoutinesRead])
def get_all_routines(limit : int = 10, skip : int = 0, search : Optional[str] = "" ):
    with database.session as sess:
        routines = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.name.contains(search)).limit(limit).offset(skip)).all()
        
        return routines

@router.post('/')
def create_routine(routine : schemas.Routine, user_id: int = Depends(oauth2.get_current_user) ):
    with database.session as sess:
        new_routine = models.Rutina(owner_id=user_id.id, **routine.dict())
        sess.add(new_routine)        
        sess.commit()
        return {'new created routine': new_routine}

@router.get('/{id}', response_model=schemas.RoutineRead)
def get_routine(id : int):
    with database.session as sess:
        routine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        return routine

@router.put('/{name}' ,response_model=schemas.RoutineRead)
def update_routine(name : str, data: schemas.RoutineUpdate, user_id: int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        q= sqlm.select(models.Rutina).where(models.Rutina.name == name)
        routine = sess.exec(q).first()

        routine.sqlmodel_update(data)

        sess.add(routine)
        sess.commit()
        sess.refresh(routine)

        return routine

@router.delete('/{name}')
def delete_routine(name : str, user_id: int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        q = sqlm.select(models.Rutina).where(models.Rutina.name == name)
        results = sess.exec(q)
        routine = results.one()
        if user_id.id != routine.owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        sess.delete(routine)
        sess.commit()
    return {"routine deleted"}