from models import models
from db import database
from schemas.exercises import ExerciseDetailsCreate, ExerciseDetailsUpdate
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from typing import Optional
from services.exercises import ExerciseService


router = APIRouter(
    prefix='/exercises',
    tags=['exercises']
)

exercise_service = ExerciseService()


@router.get('/', response_model=list)
def get_exercises(
    limit: int = 10,
    category: Optional[str] = None,
    name : Optional[str] = None
):
    """Get all available exercises, optionally filtered by category"""
    return exercise_service.get_all(limit=limit, category=category, name=name)


@router.get('/{exercise_id}', response_model=dict)
def get_exercise(exercise_id: int):
    """Get a specific exercise by ID"""
    return exercise_service.get_by_id(exercise_id)


@router.post('/{exercise_id}/details', response_model=dict, status_code=status.HTTP_201_CREATED)
def add_exercise_to_day(
    exercise_id: int,
    data: ExerciseDetailsCreate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Add an exercise to a specific training day"""
    return exercise_service.add_detail(exercise_id, data, user_id.id)


@router.get('/day/{day_id}/details', response_model=list)
def get_day_exercises(day_id: int):
    """Get all exercises assigned to a specific training day"""
    return exercise_service.get_by_day(day_id)


@router.get('/detail/{exercise_detail_id}', response_model=dict)
def get_exercise_detail(exercise_detail_id: int):
    """Get specific exercise detail by ID"""
    return exercise_service.get_detail_by_id(exercise_detail_id)


@router.put('/detail/{exercise_detail_id}', response_model=dict)
def update_exercise_detail(
    exercise_detail_id: int,
    data: ExerciseDetailsUpdate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Update an exercise detail (sets, reps, weight, etc.)"""
    return exercise_service.update_detail(exercise_detail_id, data, user_id.id)


@router.delete('/detail/{exercise_detail_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_detail(
    exercise_detail_id: int,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Remove an exercise from a training day"""
    return exercise_service.delete_detail(exercise_detail_id, user_id.id)