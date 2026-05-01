from repositories.crud import CRUDBase
from models.models import User
from dependencys import utils
from fastapi import HTTPException, status


class UserService:
    def __init__(self):
        self.crud = CRUDBase(User)
    
    def create(self, data):
        """Create a new user with password hashing"""
        hashed_password = utils.hash(data.password)
        user_data = {**data.dict(), "password": hashed_password}
        return self.crud.create(user_data)
    
    def get_by_username(self, username: str):
        """Get user by username"""
        # Since CRUDBase only supports get by ID, we need custom query
        from db import database
        import sqlmodel as sqlm
        
        with database.session as sess:
            user = sess.exec(sqlm.select(User).where(User.username == username)).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
