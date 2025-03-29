from models.emprestimo import Emprestimo
from utils.file_manager import FileManager
from controllers.livros_controller import LivrosController
from controllers.usuarios_controller import UsuariosController

class EmprestimosController:
    def __init__(self):
        self.file_manager = FileManager('emprestimos.csv', 
                                      ['ISBN', 'UserID', 'DataEmprestimo', 'DataDevolucao'])
        self.livros_ctrl = LivrosController()
        self.usuarios_ctrl = UsuariosController()

    def realizar_emprestimo(self, isbn, user_id):
        if not self.livro_disponivel(isbn):
            raise ValueError("Livro já emprestado ou não encontrado!")
        
        if not self.usuario_existe(user_id):
            raise ValueError("Usuário não encontrado!")
        
        emprestimo = Emprestimo(isbn, user_id)
        self.file_manager.add_data(emprestimo.to_dict())
        return True

    def livro_disponivel(self, isbn):
        livros = self.livros_ctrl.listar_livros()
        if not any(l['ISBN'] == isbn for l in livros):
            return False
        
        emprestimos = self.listar_emprestimos()
        return not any(e['ISBN'] == isbn and not e['DataDevolucao'] for e in emprestimos)

    def usuario_existe(self, user_id):
        usuarios = self.usuarios_ctrl.listar_usuarios()
        return any(u['ID'] == user_id for u in usuarios)

    def listar_emprestimos_ativos(self):
        emprestimos = self.listar_emprestimos()
        return [e for e in emprestimos if not e['DataDevolucao']]

    def listar_emprestimos(self):
        return self.file_manager.load_data()