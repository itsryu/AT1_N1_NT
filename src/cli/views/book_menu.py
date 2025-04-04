
from cli.views.base_menu import BaseMenu
from cli.commands.book_command import BookCommands
from dataclasses import dataclass

@dataclass
class BookMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.title = "📖 Gerenciamento de Livros"
        self.footer = "Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário"
        self.commands = BookCommands()

        self.options = {
            "1": ("Cadastrar Novo Livro", self.commands.register),
            "2": ("Listar Todos os Livros", self.commands.list_all),
            "3": ("Buscar Livros", self.commands.search),
            "4": ("Remover Livro", self.commands.remove),
            "0": ("Voltar ao Menu Principal", self.back),
        }
