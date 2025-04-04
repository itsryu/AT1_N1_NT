
from cli.views.base_menu import BaseMenu
from cli.commands.user_command import UserCommand

class UserMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.title = "📖 Gerenciamento de Usuários"
        self.footer = "Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário"
        self.commands = UserCommand()

        self.options = {
            "1": ("Cadastrar Novo Usuário", self.commands.register),
            "2": ("Listar Todos os Usuários", self.commands.list_all),
            "3": ("Buscar Usuário", self.commands.search),
            "4": ("Remover Usuário", self.commands.remove),
            "0": ("Voltar ao Menu Principal", self.back),
        }
