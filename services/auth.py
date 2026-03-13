from ..models.models import User
from ..db import database
from ..dependencys import utils, oauth2
from fastapi import HTTPException, status
import sqlmodel as sqlm
from datetime import datetime, timedelta
from ..models.models import RefreshToken

class AuthService:
    def login(self, email: str, password: str):
        with database.session as sess:
            user = sess.exec(sqlm.select(User).where(User.email == email)).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

        if not utils.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

        access_token = oauth2.create_token(data={"user_id": user.id})
        refresh_token = oauth2.create_refresh_token()

        with database.session as sess:
            db_token = RefreshToken(
                user_id=user.id,
                token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(days=oauth2.REFRESH_TOKEN_EXPIRE_DAYS)
            )
            sess.add(db_token)
            sess.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "type": "bearer"
        }