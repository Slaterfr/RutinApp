# Import all schemas and re-export them for backward compatibility
from .schemas import (
    UserCreate,
    UserResponse,
    UserInfo,
    Token,
    TokenData,
    BotRequest,
)

from .routines import (
    Routine,
    RoutinesRead,
    RoutineRead,
    RoutineUpdate,
    RoutineSearch,
)

from .days import (
    DayCreate,
    DaysRead,
    DayUpdate,
)

from .exercises import (
    ExerciseDetailsCreate,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse",
    "UserInfo",
    "Token",
    "TokenData",
    "BotRequest",
    # Routine schemas
    "Routine",
    "RoutinesRead",
    "RoutineRead",
    "RoutineUpdate",
    "RoutineSearch",
    # Day schemas
    "DayCreate",
    "DaysRead",
    "DayUpdate",
    # Exercise schemas
    "ExerciseDetailsCreate",
]
