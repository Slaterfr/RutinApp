from models import models
from db import database
from schemas.sessions import SessionCreate, SessionRead, SessionUpdate, LastSession
from dependencys import oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter, BackgroundTasks
import sqlmodel as sqlm
from typing import Optional
from datetime import date
from services.sessions import SessionService
from services.stadistics import stats_service


router = APIRouter(
    prefix='/sessions',
    tags=['Sessions']
)

session_service = SessionService()


@router.post('/', response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    session: SessionCreate,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Create a new workout session"""
    result = session_service.create(session, user_id.id)
    background_tasks.add_task(stats_service.recalculate_week_progress, user_id.id, session.session_date)
    return result


@router.get('/{session_id}', response_model=SessionRead)
def get_session(session_id: int):
    """Get specific session details"""
    return session_service.get_by_id(session_id)


@router.get('/users/{user_id}/sessions', response_model=list[SessionRead])
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


@router.get('/users/{user_id}/sessions/{session_id}', response_model=LastSession)
def get_last_session(user_id : int, session_id : int, current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these sessions")
    return session_service.get_last(user_id)


@router.put('/{session_id}', response_model=SessionRead)
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
    background_tasks: BackgroundTasks,
    user_id: int = Depends(oauth2.get_current_user)
):
    """Delete incomplete session"""
    with database.session as sess:
        session = sess.exec(sqlm.select(models.Session).where(models.Session.id == session_id)).first()
        session_date = session.session_date if session else None
    result = session_service.delete(session_id, user_id.id)
    background_tasks.add_task(stats_service.recalculate_week_progress, user_id.id, session_date)
    return result
