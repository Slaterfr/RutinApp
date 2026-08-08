from fastapi import APIRouter, Depends, status
import sqlmodel as sqlm
import json

from db import database
from dependencys import oauth2
from models.models import User, WeekProgress
from schemas.stadistics import DashboardStatsRead, HistoricalStatsRead
from services.stadistics import stats_service, get_current_week_start

router = APIRouter(
    prefix='/stadistics',
    tags=['Statistics']
)


@router.get('/dashboard', response_model=DashboardStatsRead)
def get_dashboard_statistics(current_user: User = Depends(oauth2.get_current_user)):
    """Fetch current week's quick stats, active streak, and muscle distribution"""
    with database.session as sess:
        week_start = get_current_week_start()
        progress = sess.exec(
            sqlm.select(WeekProgress)
            .where(WeekProgress.user_id == current_user.id)
            .where(WeekProgress.week_start_date == week_start)
        ).first()
        
        if not progress:
            # Recalculate on-the-fly if first time of the week
            stats_service.recalculate_week_progress(current_user.id)
            progress = sess.exec(
                sqlm.select(WeekProgress)
                .where(WeekProgress.user_id == current_user.id)
                .where(WeekProgress.week_start_date == week_start)
            ).first()
            
        if not progress:
            return DashboardStatsRead(
                total_workouts=0,
                total_volume=0.0,
                muscle_distribution={},
                active_streak=0
            )
            
        try:
            distribution = json.loads(progress.muscle_distribution)
        except Exception:
            distribution = {}

        return DashboardStatsRead(
            total_workouts=progress.total_workouts,
            total_volume=progress.total_volume,
            muscle_distribution=distribution,
            active_streak=progress.active_streak
        )


@router.get('/history', response_model=list[HistoricalStatsRead])
def get_historical_statistics(current_user: User = Depends(oauth2.get_current_user)):
    """Fetch week-by-week historical workout counts, volume, and sets progression"""
    return stats_service.get_historical_stats(current_user.id)
