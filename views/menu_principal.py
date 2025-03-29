from typing import Callable, Optional, Tuple
from views.base_view import BaseView

class MenuPrincipal(BaseView):
    def setup_ui(self) -> None:
        self.clear_frame()
        self.setup_main_frame()
        self.setup_header()
        self.setup_menu_buttons()

    def setup_main_frame(self) -> None:
        self.main_frame = self.create_frame(bg="#f0f0f0")
        self.main_frame.pack_propagate(False)
        self.main_frame.config(width=400, height=500)

    def setup_header(self) -> None:
        self.create_label(self.main_frame, "Sistema de Biblioteca Digital", font=("Arial", 16, "bold")).pack(pady=(20, 30))

    def setup_menu_buttons(self) -> None:
        buttons_info = self.get_menu_buttons_info()

        for text, color, command in buttons_info:
            self.create_menu_button(text, color, command)

    def get_menu_buttons_info(self) -> Tuple[Tuple[str, str, Optional[Callable]], ...]:
        return (
            ("Cadastro de Livros", "#4CAF50", self.abrir_livros_view),
            ("Cadastro de Usuários", "#2196F3", self.abrir_usuarios_view),
            ("Sistema de Empréstimos", "#FF9800", self.abrir_emprestimos_view),
            ("Estatísticas e Relatórios", "#9C27B0", self.abrir_estatisticas_view),
            ("Sair", "#F44336", self.sair),
        )

    def create_menu_button(
        self, text: str, color: str, command: Optional[Callable]
    ) -> None:
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

    def abrir_livros_view(self) -> None:
        from views.livros_view import LivrosView

        self.navigate_to(LivrosView)

    def abrir_usuarios_view(self) -> None:
        from views.usuarios_view import UsuariosView

        self.navigate_to(UsuariosView)

    def abrir_emprestimos_view(self) -> None:
        from views.emprestimos_view import EmprestimosView

        self.navigate_to(EmprestimosView)

    def abrir_estatisticas_view(self) -> None:
        from views.estatisticas_view import EstatisticasView

        self.navigate_to(EstatisticasView)

    def navigate_to(self, view_class: type) -> None:
        self.clear_frame()
        view_class(self.root)

    def sair(self) -> None:
        self.root.quit()

    def run(self) -> None:
        self.root.mainloop()
