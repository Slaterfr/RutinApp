from models import models
from db import database
from schemas.workoutsets import WorkoutSetCreate, WorkoutSetRead, WorkoutSetUpdate
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from typing import Optional
from services.workoutsets import WorkoutSetService


router = APIRouter(
    prefix='/sessions',
    tags=['Workout Sets']
)

workout_set_service = WorkoutSetService()


@router.post('/{session_id}/sets', response_model=dict, status_code=status.HTTP_201_CREATED)
def create_workout_set(
    session_id: int,
    data: WorkoutSetCreate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Log actual performance for a set"""
    return workout_set_service.create(session_id, data, user_id.id)


@router.get('/{session_id}/sets', response_model=list)
def get_session_sets(session_id: int):
    """Get all sets in a session"""
    return workout_set_service.get_session_sets(session_id)


@router.put('/{session_id}/sets/{set_id}', response_model=dict)
def update_workout_set(
    session_id: int,
    set_id: int,
    data: WorkoutSetUpdate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Update set performance"""
    return workout_set_service.update(set_id, data, user_id.id)


@router.delete('/{session_id}/sets/{set_id}')
def delete_workout_set(
    session_id: int,
    set_id: int,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Delete a workout set"""
    return workout_set_service.delete(set_id, user_id.id)
