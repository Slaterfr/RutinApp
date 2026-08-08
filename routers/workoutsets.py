from models import models
from db import database
from schemas.workoutsets import WorkoutSetCreate, WorkoutSetRead, WorkoutSetUpdate
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter, BackgroundTasks
import sqlmodel as sqlm
from typing import Optional
from services.workoutsets import WorkoutSetService
from services.stadistics import stats_service


router = APIRouter(
    prefix='/sessions',
    tags=['Workout Sets']
)

workout_set_service = WorkoutSetService()


@router.post('/{session_id}/sets', response_model=WorkoutSetRead, status_code=status.HTTP_201_CREATED)
def create_workout_set(
    session_id: int,
    data: WorkoutSetCreate,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Log actual performance for a set"""
    result = workout_set_service.create(session_id, data, user_id.id)
    with database.session as sess:
        session = sess.exec(sqlm.select(models.Session).where(models.Session.id == session_id)).first()
        session_date = session.session_date if session else None
    background_tasks.add_task(stats_service.recalculate_week_progress, user_id.id, session_date)
    return result


@router.get('/{session_id}/sets', response_model=list[WorkoutSetRead])
def get_session_sets(session_id: int):
    """Get all sets in a session"""
    return workout_set_service.get_session_sets(session_id)


@router.put('/{session_id}/sets/{set_id}', response_model=WorkoutSetRead)
def update_workout_set(
    session_id: int,
    set_id: int,
    data: WorkoutSetUpdate,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Update set performance"""
    result = workout_set_service.update(set_id, data, user_id.id)
    with database.session as sess:
        session = sess.exec(sqlm.select(models.Session).where(models.Session.id == session_id)).first()
        session_date = session.session_date if session else None
    background_tasks.add_task(stats_service.recalculate_week_progress, user_id.id, session_date)
    return result


@router.delete('/{session_id}/sets/{set_id}')
def delete_workout_set(
    session_id: int,
    set_id: int,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Delete a workout set"""
    result = workout_set_service.delete(set_id, user_id.id)
    with database.session as sess:
        session = sess.exec(sqlm.select(models.Session).where(models.Session.id == session_id)).first()
        session_date = session.session_date if session else None
    background_tasks.add_task(stats_service.recalculate_week_progress, user_id.id, session_date)
    return result
