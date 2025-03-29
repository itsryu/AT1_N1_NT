from models.usuario import Usuario
from utils.file_manager import FileManager

class UsuariosController:
    def __init__(self):
        self.file_manager = FileManager('usuarios.csv', 
                                      ['Nome', 'Email', 'ID', 'Tipo'])

    def cadastrar_usuario(self, usuario_data):
        usuario = Usuario(**usuario_data)
        if self.email_existe(usuario.email):
            raise ValueError("Já existe um usuário com este e-mail!")
        if self.id_existe(usuario.id_usuario):
            raise ValueError("Já existe um usuário com este ID!")
        
        self.file_manager.add_data(usuario.to_dict())
        return True

    def email_existe(self, email):
        usuarios = self.listar_usuarios()
        return any(u['Email'] == email for u in usuarios)

    def id_existe(self, id_usuario):
        usuarios = self.listar_usuarios()
        return any(u['ID'] == id_usuario for u in usuarios)

    def listar_usuarios(self):
        return self.file_manager.load_data()