from datetime import date, datetime, timedelta
import json
import sqlmodel as sqlm
from fastapi import HTTPException, status

from db import database
from models.models import Session, WorkoutSet, ExerciseDetail, Exercise, WeekProgress


class UserStatisticHistorical(sqlm.SQLModel, table=True):
    __tablename__ = "userstadistichistorical"
    
    user_id: int = sqlm.Field(primary_key=True)
    week_start_date: date = sqlm.Field(primary_key=True)
    workouts_completed: int
    total_volume: float
    total_sets: int


def get_current_week_start() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


def calculate_streak(session_dates: list[date]) -> int:
    unique_dates = sorted(list(set(session_dates)), reverse=True)
    if not unique_dates:
        return 0
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    if unique_dates[0] < yesterday and unique_dates[0] != today:
        return 0
    
    streak = 1
    current_date = unique_dates[0]
    
    for next_date in unique_dates[1:]:
        if (current_date - next_date).days == 1:
            streak += 1
            current_date = next_date
        elif (current_date - next_date).days > 1:
            break
            
    return streak


class StatisticsService:
    def recalculate_week_progress(self, user_id: int, target_date: date = None):
        """Recalculates stats for the week containing target_date, updates weekprogress table"""
        if target_date is None:
            target_date = date.today()

        with database.session as sess:
            week_start = target_date - timedelta(days=target_date.weekday())
            week_end = week_start + timedelta(days=6)
            
            # 1. Total workouts this week
            workouts_query = (
                sqlm.select(Session)
                .where(Session.user_id == user_id)
                .where(Session.session_date >= week_start)
                .where(Session.session_date <= week_end)
            )
            sessions_this_week = sess.exec(workouts_query).all()
            total_workouts = len(sessions_this_week)
            
            # 2. Total volume and muscle distribution this week
            session_ids = [s.id for s in sessions_this_week]
            total_volume = 0.0
            muscle_counts = {}
            
            if session_ids:
                sets_query = (
                    sqlm.select(WorkoutSet)
                    .where(WorkoutSet.session_id.in_(session_ids))
                )
                sets_this_week = sess.exec(sets_query).all()
                
                for wset in sets_this_week:
                    total_volume += (wset.reps * wset.weight)
                    
                    if wset.exercise_detail_id:
                        detail = sess.exec(
                            sqlm.select(ExerciseDetail)
                            .where(ExerciseDetail.id == wset.exercise_detail_id)
                        ).first()
                        if detail and detail.exercise_id:
                            exercise = sess.exec(
                                sqlm.select(Exercise)
                                .where(Exercise.id == detail.exercise_id)
                            ).first()
                            if exercise and exercise.muscles:
                                muscles = [
                                    m.strip().capitalize()
                                    for m in exercise.muscles.replace('{', '').replace('}', '').split(',')
                                    if m.strip()
                                ]
                                for muscle in muscles:
                                    muscle_counts[muscle] = muscle_counts.get(muscle, 0) + 1
            
            # 3. Active Streak (all sessions)
            all_sessions = sess.exec(
                sqlm.select(Session.session_date)
                .where(Session.user_id == user_id)
            ).all()
            active_streak = calculate_streak(all_sessions)
            
            # 4. Save to database
            progress = sess.exec(
                sqlm.select(WeekProgress)
                .where(WeekProgress.user_id == user_id)
                .where(WeekProgress.week_start_date == week_start)
            ).first()
            
            if not progress:
                progress = WeekProgress(
                    user_id=user_id,
                    week_start_date=week_start,
                    total_workouts=total_workouts,
                    total_volume=total_volume,
                    muscle_distribution=json.dumps(muscle_counts),
                    active_streak=active_streak,
                    updated_at=datetime.utcnow()
                )
                sess.add(progress)
            else:
                progress.total_workouts = total_workouts
                progress.total_volume = total_volume
                progress.muscle_distribution = json.dumps(muscle_counts)
                progress.active_streak = active_streak
                progress.updated_at = datetime.utcnow()
                sess.add(progress)
                
            sess.commit()

    def get_historical_stats(self, user_id: int) -> list[UserStatisticHistorical]:
        """Gets historical week-by-week aggregated stats from userstadistichistorical view"""
        with database.session as sess:
            results = sess.exec(
                sqlm.select(UserStatisticHistorical)
                .where(UserStatisticHistorical.user_id == user_id)
                .order_by(UserStatisticHistorical.week_start_date.asc())
            ).all()
            return results


stats_service = StatisticsService()
