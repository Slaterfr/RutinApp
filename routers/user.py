from models import models
from db import database
from schemas import UserCreate, UserResponse, UserInfo
from dependencys import utils
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm
from services.users import UserService

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

user_service = UserService()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user : UserCreate):
    return user_service.create(user)

@router.get('/{username}', response_model=UserInfo)
def get_user_profile(username : str):
    return user_service.get_by_username(username)