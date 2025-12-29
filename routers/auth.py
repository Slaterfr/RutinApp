from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import sqlmodel as sqlm

from ..db import database, models
from .. import schemas, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)



@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends()):
    with database.session as sess:
        user = sess.exec(sqlm.select(models.User).where(models.User.email == user_credentials.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_token(data = {"user_id" : user.id})

    return {"token" : access_token, "type": "bearer"}