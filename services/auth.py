from ..models.models import User
from ..db import database
from ..dependencys import utils, oauth2
from fastapi import HTTPException, status
import sqlmodel as sqlm


class AuthService:
    def login(self, email: str, password: str):
        """Authenticate user and generate token"""
        with database.session as sess:
            user = sess.exec(sqlm.select(User).where(User.email == email)).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        
        if not utils.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        
        access_token = oauth2.create_token(data={"user_id": user.id})
        return {"token": access_token, "type": "bearer"}
