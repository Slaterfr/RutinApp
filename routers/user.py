from .. import models, schemas, utils, database
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate):
    with database.session as sess:
        print("PASSWORD:", user.password, type(user.password), len(user.password))

        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        new_user = models.User(**user.dict())
        sess.add(new_user)
        sess.commit()
        sess.refresh(new_user)

        return new_user