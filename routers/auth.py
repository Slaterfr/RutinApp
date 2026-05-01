from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import date, datetime

from models import models
from db import database
from schemas.schemas import RefreshRequest
from dependencys import utils, oauth2
from services.auth import AuthService

router = APIRouter(
    tags=['Authentication']
)

auth_service = AuthService()


@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends()):
    return auth_service.login(user_credentials.username, user_credentials.password)


@router.post("/refresh")
def refresh(body: RefreshRequest):
    with database.session as sess:
        db_token = sess.exec(
            select(models.RefreshToken).where(models.RefreshToken.token == body.refresh_token)
        ).first()

        if not db_token or db_token.revoked or db_token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        new_access_token = oauth2.create_token(data={"user_id": db_token.user_id})
        return {"access_token": new_access_token, "type": "bearer"}


@router.post("/logout")
def logout(body: RefreshRequest):
    with database.session as sess:
        db_token = sess.exec(
            select(models.RefreshToken).where(models.RefreshToken.token == body.refresh_token)
        ).first()

        if not db_token or db_token.revoked:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

        db_token.revoked = True
        sess.add(db_token)
        sess.commit()

    return {"detail": "Logged out successfully"}