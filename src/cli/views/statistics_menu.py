from cli.views.base_menu import BaseMenu
from cli.commands.statistics_command import StatisticsCommand
from dataclasses import dataclass

@dataclass
class StatisticsMenu(BaseMenu):
    def __init__(self):
        super().__init__()

        self.title = "📊 Estatísticas do Sistema"
        self.footer = "Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário"
        self.commands = StatisticsCommand()

        self.options = {
            "1": ("Listar Livros Por Categoria", self.commands.show_books_by_category),
            "2": ("Listar Empréstimos Por Tipo de Usuário", self.commands.show_loans_by_user_type),
            "3": ("Listar Livros Mais Emprestados", self.commands.show_most_loaned_books),
            "4": ("Gerar Relatório em PDF", self.commands.generate_pdf_report),
            "0": ("Voltar ao Menu Principal", self.back),
        }