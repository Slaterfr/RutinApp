from ..db import database, models
from .. import schemas, utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
import sqlalchemy
from typing import Optional


router = APIRouter(
    prefix='/exercises',
    tags=['exercises']
)


@router.get('/')
def get_exercises(limit : int = 6, category : Optional[str] = ''):
    with database.session as sess:
        exercises = sess.exec(sqlm.select(models.Ejercicio).where(models.Ejercicio.category.contains(category)).limit(limit)).all()
        return exercises
    
@router.post('/{exercise_id}')
def add_exercise(exercise_id : int, data : schemas.ExerciseDetailsCreate):
    with database.session as sess:
        exercise = sess.exec(sqlm.select(models.Ejercicio).where(models.Ejercicio.id==exercise_id)).first()
        new_exercise = models.detalleEjercicio(exersise_id=exercise_id, name=exercise.exersise_name, equipment_needed=exercise.equipment_needed, **data.dict())
        sess.add(new_exercise)
        sess.commit()
        return new_exercise

@router.get('/{day_id}/exercises_details')
def get_days_exercises(day_id : int):
    with database.session as sess:
        day = sess.exec(sqlm.select(models.DiaRutina).where(models.DiaRutina.id==day_id)).first()
        exercises = day.exercises
        return exercises