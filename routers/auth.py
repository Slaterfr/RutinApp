from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import sqlmodel as sqlm

from ..models import models
from ..db import database
from ..schemas import Token
from ..dependencys import utils, oauth2
from ..services.auth import AuthService

router = APIRouter(
    tags=['Authentication']
)

auth_service = AuthService()


@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends()):
    return auth_service.login(user_credentials.username, user_credentials.password)