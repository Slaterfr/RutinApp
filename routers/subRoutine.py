from .. import models, schemas, utils, database, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from sqlmodel import join




router = APIRouter(
    prefix='/routines',
    tags=['subroutines']
)

@router.post('/{id}/create_day')
def post_day(data : schemas.DayCreate, id : int, user_id: int = Depends(oauth2.get_current_user)):
    with database.session as sess:
        currentRoutine = sess.exec(sqlm.select(models.Rutina).where(models.Rutina.id == id)).one()
        if currentRoutine.owner_id != user_id.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        new_day = models.DiaRutina(routine_id=currentRoutine.id, **data.dict())
        sess.add(new_day)
        sess.commit()
    return new_day


