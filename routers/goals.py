from fastapi import FastAPI, APIRouter, HTTPException, Depends
from services.goals import GoalsService
from schemas import goals as schemas
from dependencys.oauth2 import get_current_user

router = APIRouter(
    prefix= "/goals",
    tags=['Goals']
)


@router.get('/', response_model=schemas.GoalRead)
def read_all(user_id : int = Depends(get_current_user)):
    
    return GoalsService.read_goals()
