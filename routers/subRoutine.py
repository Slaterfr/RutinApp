from models import models
from db import database
from schemas import DayCreate, DayUpdate
from dependencys import utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from sqlmodel import join
from services.subroutines import SubRoutineService


router = APIRouter(
    prefix='/routines',
    tags=['subroutines']
)

subroutine_service = SubRoutineService()

@router.get('/{id}/days')
def get_days(id : int):
    return subroutine_service.get_days(id)


@router.post('/{id}/days')
def post_day(data : DayCreate, id : int, user_id: int = Depends(oauth2.get_current_user)):
    return subroutine_service.create_day(id, data, user_id.id)


@router.put('/{id}/days/{day_id}')
def update_day(data : DayUpdate, id: int, day_id : int, user_id: int = Depends(oauth2.get_current_user)):
    return subroutine_service.update_day(id, day_id, data, user_id.id)
        

@router.delete('/{id}/days/{day_id}')
def delete_day(id : int, day_id : int, user_id : int = Depends(oauth2.get_current_user)):
    return subroutine_service.delete_day(id, day_id, user_id.id)
