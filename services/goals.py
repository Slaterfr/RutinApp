from repositories.crud import CRUDBase
from models.models import Goal

class GoalsService:
    def __init__(self):
        self.GoalsCrud = CRUDBase(Goal)

    def create_goal(self, data: dict, user_id : int):
        return self.GoalsCrud.create(data, user_id)
    
    def read_goals(self):
        return self.GoalsCrud.read_all()
    
    def read_one(self, id : int):
        return self.GoalsCrud.read(id)
    
    def delete(self, id : int):
        return self.GoalsCrud.delete(id)
    
    