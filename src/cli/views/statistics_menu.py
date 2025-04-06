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
            "1": ("Livros por Categoria (Tabela)", lambda: self.commands.show_books_by_category('table')),
            "2": ("Livros por Categoria (Gráfico de Barras)", lambda: self.commands.show_books_by_category('bar')),
            "3": ("Empréstimos por Tipo de Usuário (Tabela)", lambda: self.commands.show_loans_by_user_type('table')),
            "4": ("Empréstimos por Tipo de Usuário (Gráfico)", lambda: self.commands.show_loans_by_user_type('bar')),
            "5": ("Livros Mais Emprestados", self.commands.show_most_loaned_books),
            "6": ("Gerar Relatório PDF", self.commands.generate_pdf_report),
            "0": ("Voltar", self.back)
        }
