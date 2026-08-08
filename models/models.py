from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from typing import Optional
from datetime import date, datetime


# ─── USER ───────────────────────────────────────────────────────────────────

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: Optional[str] = None
    biography: Optional[str] = None
    email: EmailStr
    password: str
    routines: list["Routine"] = Relationship(back_populates="owner")
    goals: list["Goal"] = Relationship(back_populates="owner")


# ─── CATALOGS ────────────────────────────────────────────────────────────────

class Physique(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    img_url: str
    description: str


class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_name: str
    instructions: str
    equipment_needed: str
    category: str
    muscles : str
    external_id : str | None = Field(default=None, unique=True)


# ─── GOALS ───────────────────────────────────────────────────────────────────

class Goal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    owner: User | None = Relationship(back_populates="goals")
    current_weight: float
    goal_weight: float
    current_physique_id: int | None = Field(default=None, foreign_key="physique.id")
    goal_physique_id: int | None = Field(default=None, foreign_key="physique.id")
    priority: int = Field(default=3)  # 1 = highest, 2 = medium, 3 = lowest
    notes: Optional[str] = None
    created_at: date = Field(default_factory=date.today)
    achieved_at: Optional[date] = None


# ─── ROUTINES ────────────────────────────────────────────────────────────────

class Routine(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    days_per_week: int
    estimated_hours: float
    is_template: bool = Field(default=False)
    owner_id: int | None = Field(default=None, foreign_key="user.id")
    owner: User | None = Relationship(back_populates="routines")
    days: list["RoutineDay"] = Relationship(back_populates="routine")
    sessions: list["Session"] = Relationship(back_populates="routine")


class RoutineDay(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    routine_id: int | None = Field(default=None, foreign_key="routine.id")
    routine: Routine | None = Relationship(back_populates="days")
    day_number: int
    day_name: str
    focus_area: str
    exercises: list["ExerciseDetail"] = Relationship(back_populates="day")


class ExerciseDetail(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    day_id: int | None = Field(default=None, foreign_key="routineday.id")
    day: RoutineDay | None = Relationship(back_populates="exercises")
    set_count: int
    rep_target: int
    rest_seconds: int
    weight_notes: Optional[str] = None
    sets: list["WorkoutSet"] = Relationship(back_populates="exercise_detail")


# ─── SESSIONS ────────────────────────────────────────────────────────────────

class Session(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    routine_id: int | None = Field(default=None, foreign_key="routine.id")
    routine: Routine | None = Relationship(back_populates="sessions")
    day_id: int | None = Field(default=None, foreign_key="routineday.id")
    session_date: date = Field(default_factory=date.today)
    notes: Optional[str] = None
    sets: list["WorkoutSet"] = Relationship(back_populates="session")


class WorkoutSet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: int | None = Field(default=None, foreign_key="session.id")
    session: Session | None = Relationship(back_populates="sets")
    exercise_detail_id: int | None = Field(default=None, foreign_key="exercisedetail.id")
    exercise_detail: ExerciseDetail | None = Relationship(back_populates="sets")
    set_number: int
    reps: int
    weight: float
    notes: Optional[str] = None

# --- Refresh Toekn -----------------
class RefreshToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ─── STATISTICS ──────────────────────────────────────────────────────────────

class WeekProgress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    week_start_date: date
    total_workouts: int = Field(default=0)
    total_volume: float = Field(default=0.0)
    muscle_distribution: str = Field(default="{}")
    active_streak: int = Field(default=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)