from ...db import database
from ...models import models
from ...schemas import UserCreate, UserResponse, UserInfo
from ...dependencys import utils
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
import sqlmodel as sqlm

router = APIRouter(
    prefix='/users',
    tags=['Users']
)



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user : UserCreate):
    with database.session as sess:

        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        new_user = models.User(**user.dict())
        sess.add(new_user)
        sess.commit()
        sess.refresh(new_user)

        return new_user
    

@router.get('/{username}', response_model=UserInfo)
def get_user_profile(username : str):
    with database.session as sess:
        user = sess.exec(sqlm.select(models.User).where(models.User.username==username)).one()

        return  user