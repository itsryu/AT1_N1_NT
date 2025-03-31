from typing import List, Dict
import re
from models.user import User
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

class UsersController(BaseController[User]):
    def __init__(self) -> None:
        super().__init__(FileManager(
            filename='data/users.csv',
            headers=['Name', 'Email', 'ID', 'Type'],
            model_class=User
        ))

    def search_term(self, term: str) -> List[User]:
        term_lower = term.lower()
        
        return [
            user for user in self.list_all()
            if term_lower in user.Name.lower() or 
               term_lower in user.Email.lower() or 
               term_lower in user.Type.lower() or
               term_lower in user.ID.lower()
        ]
    
    def get_user_by_id(self, user_id: str) -> User:
        users = self.list_all()

        for user in users:
            if user.ID == user_id:
                return user
        raise ValueError("User not found!")
    
    def register_user(self, user_data: Dict[str, str]) -> None:
        if (not user_data.get("Name") or 
            not user_data.get("Email") or 
            not user_data.get("ID") or 
            not user_data.get("Type")):
            raise ValueError("All fields are required!")
        elif self.email_exists(user_data["Email"]):
            raise ValueError("Email already registered!")
        elif self.id_exists(user_data["ID"]):
            raise ValueError("ID already registered!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", user_data["Email"]):
            raise ValueError("Invalid email!")
        
        user = User(**user_data)
        self.add(user)

    def delete_user(self, user_id: str) -> None:
        users = self.list_all()
        user_to_remove = None

        for user in users:
            if user.ID == user_id:
                user_to_remove = user
                break

        if user_to_remove:
            self.remove(user_to_remove)
        else:
            raise ValueError("User not found!")

    def email_exists(self, email: str) -> bool:
        return any(user.Email == email for user in self.list_all())

    def id_exists(self, user_id: str) -> bool:
        return any(user.ID == user_id for user in self.list_all())