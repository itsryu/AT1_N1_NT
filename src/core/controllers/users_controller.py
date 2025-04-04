from typing import List, Dict
import re
from core.models.user import User
from shared.file_manager import FileManager
from core.controllers.base_controller import BaseController

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
            if any(term_lower in getattr(user, attr).lower() for attr in ['Name', 'Email', 'Type', 'ID'])
        ]

    def get_user_by_id(self, user_id: str) -> User:
        user = next((user for user in self.list_all() if str(user.ID).strip() == user_id.strip()), None)
        if not user:
            raise ValueError("Usuário não encontrado!")
        return user

    def register_user(self, user_data: Dict[str, str]) -> None:
        required_fields = ["Name", "Email", "ID", "Type"]
        missing_fields = [field for field in required_fields if not user_data.get(field)]

        if missing_fields:
            raise ValueError("Todos os campos são obrigatórios!")
        elif self.email_exists(user_data["Email"]):
            raise ValueError("Email já cadastrado!")
        elif self.id_exists(user_data["ID"]):
            raise ValueError("ID já cadastrado!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", user_data["Email"]):
            raise ValueError("Email inválido!")
        
        self.add(User(**user_data))

    def delete_user(self, user_id: str) -> None:
        user_to_remove = next((user for user in self.list_all() if str(user.ID).strip() == user_id.strip()), None)
        if not user_to_remove:
            raise ValueError("Usuário não encontrado!")
        self.remove(user_to_remove)

    def email_exists(self, email: str) -> bool:
        return any(user.Email == email for user in self.list_all())

    def id_exists(self, user_id: str) -> bool:
        return any(user.ID == user_id for user in self.list_all())