from typing import Dict, List, Tuple
from collections import defaultdict
from controllers.livros_controller import LivrosController
from controllers.usuarios_controller import UsuariosController
from controllers.emprestimos_controller import EmprestimosController

class EstatisticasController:
    def __init__(self):
        self.livros_ctrl = LivrosController()
        self.usuarios_ctrl = UsuariosController()
        self.emprestimos_ctrl = EmprestimosController()

    def livros_por_categoria(self) -> Dict[str, int]:
        categorias = defaultdict(int)
        for livro in self.livros_ctrl.list_all():
            categorias[livro.Categoria] += 1
        return dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True))

    def emprestimos_por_tipo(self) -> Dict[str, int]:
        usuarios = {u.ID: u.Tipo for u in self.usuarios_ctrl.list_all()}
        tipos = defaultdict(int)
        
        for emp in self.emprestimos_ctrl.list_all():
            tipo = usuarios.get(emp.UserID, 'Visitante')
            tipos[tipo] += 1
            
        return dict(sorted(tipos.items(), key=lambda item: item[1], reverse=True))

    def livros_mais_emprestados(self, limit: int = 10) -> List[Tuple[str, str, int]]:
        livros = {l.ISBN: l.Título for l in self.livros_ctrl.list_all()}
        contagem = defaultdict(int)
        
        for emp in self.emprestimos_ctrl.list_all():
            contagem[emp.ISBN] += 1
        
        return sorted(
            [(livros.get(isbn, 'Visitante'), isbn, count) 
             for isbn, count in contagem.items()],
            key=lambda x: x[2], reverse=True
        )[:limit]