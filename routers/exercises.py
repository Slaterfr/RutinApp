from ..models import models
from ..db import database
from ..schemas import ExerciseDetailsCreate
from ..dependencys import utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
import sqlalchemy
from typing import Optional
from ..services.exercises import ExerciseService


router = APIRouter(
    prefix='/exercises',
    tags=['exercises']
)

exercise_service = ExerciseService()


@router.get('/')
def get_exercises(limit : int = 6, category : Optional[str] = ''):
    return exercise_service.get_all(limit=limit, category=category)
    
@router.post('/{exercise_id}')
def add_exercise(exercise_id : int, data : ExerciseDetailsCreate):
    return exercise_service.add_detail(exercise_id, data)

@router.get('/{day_id}/exercises_details')
def get_days_exercises(day_id : int):
    return exercise_service.get_by_day(day_id)