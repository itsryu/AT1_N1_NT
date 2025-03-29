from typing import List
from models.usuario import Usuario
from utils.file_manager import FileManager
from controllers.base_controller import BaseController
from typing import Dict
import re

class UsuariosController(BaseController[Usuario]):
    def __init__(self):
        super().__init__(FileManager(
            filename='data/usuarios.csv',
            headers=['Nome', 'Email', 'ID', 'Tipo'],
            model_class=Usuario
        ))

    def buscar_por_termo(self, termo: str) -> List[Usuario]:
        termo = termo.lower()
        return [
            usuario for usuario in self.list_all()
            if termo in usuario.Nome.lower() or 
               termo in usuario.Email.lower() or 
               termo in usuario.Tipo.lower()
        ]
    
    def cadastrar_usuario(self, usuario_data: Dict[str, str]) -> None:
        if (not usuario_data.get("Nome") or 
            not usuario_data.get("Email") or 
            not usuario_data.get("ID") or 
            not usuario_data.get("Tipo")):
            raise ValueError("Todos os campos são obrigatórios!")
        elif self.email_existe(usuario_data["Email"]):
            raise ValueError("Email já cadastrado!")
        elif self.id_existe(usuario_data["ID"]):
            raise ValueError("ID já cadastrado!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", usuario_data["Email"]):
            raise ValueError("Email inválido!")
        
        usuario = Usuario(**usuario_data)
        self.add(usuario)

    def email_existe(self, email: str) -> bool:
        return any(usuario.Email == email for usuario in self.list_all())

    def id_existe(self, id_usuario: str) -> bool:
        return any(usuario.ID == id_usuario for usuario in self.list_all())