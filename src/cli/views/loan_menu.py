from cli.views.base_menu import BaseMenu
from cli.commands.loan_command import LoanCommand
from dataclasses import dataclass

@dataclass
class LoanMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.title = "📚 Gerenciamento de Empréstimos"
        self.footer = "Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário"
        self.commands = LoanCommand()

        self.options = {
            "1": ("Registrar Novo Empréstimo", self.commands.register),
            "2": ("Registrar Devolução", self.commands.register_return),
            "3": ("Empréstimos Ativos", self.commands.list_active),
            "4": ("Histórico de Devoluções", self.commands.list_returned),
            "0": ("Voltar ao Menu Principal", self.back),   
        }