from models import models
from db import database
from schemas.sessions import SessionCreate, SessionRead, SessionUpdate
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from typing import Optional
from datetime import date
from services.sessions import SessionService


router = APIRouter(
    prefix='/sessions',
    tags=['Sessions']
)

session_service = SessionService()


@router.post('/', response_model=dict, status_code=status.HTTP_201_CREATED)
def create_session(
    session: SessionCreate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Create a new workout session"""
    return session_service.create(session, user_id.id)


@router.get('/{session_id}', response_model=dict)
def get_session(session_id: int):
    """Get specific session details"""
    return session_service.get_by_id(session_id)


@router.get('/users/{user_id}/sessions', response_model=list)
def get_user_sessions(
    user_id: int,
    limit: int = 10,
    skip: int = 0,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: int = Depends(oauth2.get_current_user)
):
    """Get all sessions for a user (paginated with optional date filtering)"""
    # Only users can view their own sessions, admins can view any
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these sessions")
    
    return session_service.get_user_sessions(user_id, skip=skip, limit=limit, start_date=start_date, end_date=end_date)


@router.put('/{session_id}', response_model=dict)
def update_session(
    session_id: int,
    data: SessionUpdate,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Update session notes or date"""
    return session_service.update(session_id, data, user_id.id)


@router.delete('/{session_id}')
def delete_session(
    session_id: int,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Delete incomplete session"""
    return session_service.delete(session_id, user_id.id)
