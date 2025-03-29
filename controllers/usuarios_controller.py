from typing import List
from models.usuario import Usuario
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

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
    
    def cadastrar_usuario(self, usuario: Usuario) -> None:
        if self.email_existe(usuario.Email):
            raise ValueError("E-mail já cadastrado!")
        if self.id_existe(usuario.ID):
            raise ValueError("ID já cadastrado!")
        self.add(usuario)

    def email_existe(self, email: str) -> bool:
        return any(usuario.Email == email for usuario in self.list_all())

    def id_existe(self, id_usuario: str) -> bool:
        return any(usuario.ID == id_usuario for usuario in self.list_all())