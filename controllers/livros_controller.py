from typing import List
from models.livro import Livro
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

class LivrosController(BaseController[Livro]):
    def __init__(self):
        super().__init__(FileManager(
            filename='data/livros.csv',
            headers=['Título', 'Autor', 'Ano', 'ISBN', 'Categoria'],
            model_class=Livro
        ))

    def buscar_por_termo(self, termo: str) -> List[Livro]:
        termo = termo.lower()

        return [
            livro for livro in self.list_all()

            if termo in livro.Título.lower() or 
               termo in livro.Autor.lower() or 
               termo in livro.Categoria.lower() or
               termo in livro.Ano.lower() or
               termo in livro.ISBN.lower()
        ]
    
    def cadastrar_livro(self, livro: Livro) -> None:
        self.add(livro)

    def isbn_existe(self, isbn: str) -> bool:
        return any(livro.ISBN == isbn for livro in self.list_all())