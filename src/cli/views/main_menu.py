from cli.views.base_menu import BaseMenu
from cli.views.book_menu import BookMenu
from cli.views.user_menu import UserMenu
from cli.views.loan_menu import LoanMenu
from cli.views.statistics_menu import StatisticsMenu

class MainMenu(BaseMenu):
    def __init__(self):
        super().__init__()
        
        self.title = "📚 Biblioteca Digital"
        
        self.options = {
            "1": ("Gerenciamento de Livros", self._show_book_menu),
            "2": ("Gerenciamento de Usuários", self._show_user_menu),
            "3": ("Gerenciamento de Empréstimos", self._show_loan_menu),
            "4": ("Estatísticas e Relatórios", self._show_statistics_menu),
            "0": ("Sair", self._exit)
        }

    def _show_book_menu(self):
        try:
            self.book_menu = BookMenu()
            self.book_menu.display()
        except StopIteration:
            pass

    def _show_user_menu(self):
        try:
            self.user_menu = UserMenu()
            self.user_menu.display()
        except StopIteration:
            pass

    def _show_loan_menu(self):
        try:
            self.loan_menu = LoanMenu()
            self.loan_menu.display()
        except StopIteration:
            pass

    def _show_statistics_menu(self):
        try:
            self.statistics_menu = StatisticsMenu()
            self.statistics_menu.display()
        except StopIteration:
            pass
    
    def _not_implemented(self):
        self.console.print("\n[yellow]Funcionalidade em desenvolvimento![/yellow]")
        input("Pressione Enter para continuar...")
    
    def _exit(self):
        self.console.print("\n[green]Até logo![/green]")
        raise SystemExit