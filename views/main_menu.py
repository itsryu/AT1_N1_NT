from typing import Callable, Optional, Tuple
from views.base_view import BaseView
from utils.helpers import handle_errors
from utils.logger import Logger

class MainMenu(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.initialize_main_frame()
        self.initialize_header()
        self.initialize_menu_buttons()

    @handle_errors
    def initialize_main_frame(self) -> None:
        self.main_frame = self.create_frame(bg="#f0f0f0")
        self.main_frame.pack_propagate(False)
        self.main_frame.config(width=400, height=500)

    @handle_errors
    def initialize_header(self) -> None:
        self.create_label(
            self.main_frame,
            "Sistema de Biblioteca Digital",
            font=("Arial", 16, "bold")
        ).pack(pady=(20, 30))

    def initialize_menu_buttons(self) -> None:
        buttons_config = self.menu_buttons_info()
        for text, color, command in buttons_config:
            self.build_menu_button(text, color, command)

    def menu_buttons_info(self) -> Tuple[Tuple[str, str, Optional[Callable]], ...]:
        return (
            ("Cadastro de Livros", "#4CAF50", self.open_books_view),
            ("Cadastro de Usuários", "#2196F3", self.open_users_view),
            ("Sistema de Empréstimos", "#FF9800", self.open_loans_view),
            ("Estatísticas e Relatórios", "#9C27B0", self.open_statistics_view),
            ("Sair", "#F44336", self.exit_app),
        )

    def build_menu_button(self, text: str, color: str, command: Optional[Callable]) -> None:
        self.create_button(
            self.main_frame,
            text=text,
            command=command,
            bg=color,
            fg="white",
            width=25,
            height=2,
            font=("Arial", 12),
        ).pack(pady=8)

    def open_books_view(self) -> None:
        from views.books_view import BooksView
        self.navigate_to_view(BooksView)

    def open_users_view(self) -> None:
        from views.users_view import UsersView
        self.navigate_to_view(UsersView)

    def open_loans_view(self) -> None:
        from views.loans_view import LoansView
        self.navigate_to_view(LoansView)

    def open_statistics_view(self) -> None:
        from views.statistics_view import StatisticsView
        self.navigate_to_view(StatisticsView)

    def navigate_to_view(self, view_class: type) -> None:
        self.clear_frame()
        view_class(self.root)

    def exit_app(self) -> None:
        self.root.quit()

    def start_app(self) -> None:
        Logger.info("Iniciando o aplicativo...")
        self.root.mainloop()