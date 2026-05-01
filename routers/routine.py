from models import models
from db import database
from schemas import Routine, RoutinesRead, RoutineRead, RoutineUpdate
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
import sqlalchemy
from typing import Optional
from services.routines import RoutineService
from services.handlers import InvalidData


router = APIRouter(
    prefix='/routines',
    tags=['Routines']
)

routine_service = RoutineService()


@router.get('/', response_model=list[RoutinesRead])
def get_all_routines(limit : int = 10, skip : int = 0, search : Optional[str] = "" ):
    return routine_service.get_all(skip=skip, limit=limit, search=search)

@router.post('/')
def create_routine(routine : Routine, user_id: int = Depends(oauth2.get_current_user) ):
    return routine_service.create(routine, user_id.id)

@router.get('/{id}', response_model=RoutineRead)
def get_routine(id : int):
    return routine_service.get_by_id(id)

@router.put('/{routine_id}' ,response_model=RoutineRead)
def update_routine(routine_id : int, data: RoutineUpdate, user_id: int = Depends(oauth2.get_current_user)):
    return routine_service.update(routine_id, data, user_id.id)

@router.delete('/{routine_id}')
def delete_routine(routine_id : int, user_id: int = Depends(oauth2.get_current_user)):
    return routine_service.delete(routine_id, user_id.id)