from sqlmodel import SQLModel as sqlm
from sqlmodel import select

from ..models import models
from ..db import database
from typing import Type, TypeVar, Generic

ModelType = TypeVar("ModelType", bound=sqlm)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model : Type[ModelType]):
        self.model = model

    def create(self, data: dict):
        """Create a new record"""
        with database.session as sess:
            item = self.model(**data)
            sess.add(item)
            sess.commit()
            sess.refresh(item)
        return item
    
    def read(self, id: int):
        """Read a single record by ID"""
        with database.session as sess:
            return sess.exec(select(self.model).where(self.model.id == id)).first()

    def read_all(self, skip: int = 0, limit: int = 10):
        """Read all records with pagination"""
        with database.session as sess:
            return sess.exec(select(self.model).offset(skip).limit(limit)).all()

    def update(self, id: int, data: dict):
        """Update a record by ID"""
        with database.session as sess:
            item = sess.exec(select(self.model).where(self.model.id == id)).first()
            if not item:
                return None
            item.sqlmodel_update(data)
            sess.add(item)
            sess.commit()
            sess.refresh(item)
            return item
        
    def delete(self, id: int):
        """Delete a record by ID"""
        with database.session as sess:
            item = sess.exec(select(self.model).where(self.model.id == id)).first()
            if not item:
                return False
            sess.delete(item)
            sess.commit()
            return True
        

        
    
        




