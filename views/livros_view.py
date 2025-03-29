from typing import Dict, List
from models.livro import Livro
from controllers.livros_controller import LivrosController
from views.base_view import BaseView
import tkinter as tk

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].show_error(f"Ocorreu um erro em '{func.__name__}': {e}")

    return wrapper

class LivrosView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = LivrosController()

        main_frame = self.create_frame(bg="#f0f0f0")
        self.setup_cadastro_section(main_frame)
        self.setup_busca_section(main_frame)
        self.setup_results_table(main_frame)
        self.setup_back_button(main_frame)

        self.carregar_livros()

    @handle_errors
    def setup_cadastro_section(self, parent: tk.Widget) -> None:
        frame_cadastro = self.create_frame(parent, bg="#f0f0f0")
        self.create_label(frame_cadastro, "Cadastro de Livros", font=("Arial", 14)).pack(pady=10)

        self.entries = self.create_form_fields(frame_cadastro)
        self.create_action_buttons(frame_cadastro)

    @handle_errors
    def create_form_fields(self, parent: tk.Widget) -> Dict[str, tk.Entry]:
        fields = ["Título", "Autor", "Ano", "ISBN", "Categoria"]
        entries = {}

        for field in fields:
            row_frame = tk.Frame(parent, bg="#f0f0f0")
            row_frame.pack(fill="x", pady=5)

            self.create_label(row_frame, field, width=10, anchor="e").pack(side="left", padx=5)
            entries[field] = self.create_entry(row_frame)
            entries[field].pack(side="left", padx=5)

        return entries

    @handle_errors
    def create_action_buttons(self, parent: tk.Widget) -> None:
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)

        self.create_button(btn_frame, "Salvar Livro", self.salvar_livro, bg="#4CAF50").pack(side="left", padx=5)

        self.create_button(btn_frame, "Limpar", self.limpar_campos, bg="#607D8B").pack(side="left", padx=5)

    @handle_errors
    def setup_busca_section(self, parent: tk.Widget) -> None:
        frame_busca = self.create_frame(parent, bg="#f0f0f0")

        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.entry_busca = self.create_entry(search_frame)
        self.entry_busca.pack(side="left", padx=5)

        self.create_button(search_frame, "Buscar", self.buscar_livros, bg="#4CAF50", width=10).pack(side="left", padx=5)

    @handle_errors
    def setup_results_table(self, parent: tk.Widget) -> None:
        self.tree = self.create_treeview(parent, columns=["Título", "Autor", "Ano", "ISBN", "Categoria"])
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    @handle_errors
    def setup_back_button(self, parent: tk.Widget) -> None:
        self.create_button(parent, "Voltar ao Menu", self.voltar_menu, bg="#F44336").pack(pady=10)

    @handle_errors
    def salvar_livro(self) -> None:
        livro_data = {field: self.entries[field].get() for field in self.entries}
        livro = Livro(**livro_data)

        try:
            self.controller.cadastrar_livro(livro)
            self.show_success("Livro cadastrado com sucesso!")
            self.carregar_livros()
            self.limpar_campos()
        except ValueError as e:
            self.show_error(str(e))

    @handle_errors
    def limpar_campos(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, "end")

    @handle_errors
    def buscar_livros(self) -> None:
        termo = self.entry_busca.get()
        resultados = self.controller.buscar_por_termo(termo)
        self.mostrar_resultados(resultados)

    @handle_errors
    def carregar_livros(self) -> None:
        livros = self.controller.list_all()
        self.mostrar_resultados(livros)

    @handle_errors
    def mostrar_resultados(self, livros: List[Livro]) -> None:
        self.tree.delete(*self.tree.get_children())
        for livro in livros:
            self.tree.insert(
                "",
                "end",
                values=[
                    livro.Título,
                    livro.Autor,
                    livro.Ano,
                    livro.ISBN,
                    livro.Categoria,
                ],
            )

    @handle_errors
    def voltar_menu(self) -> None:
        from views.menu_principal import MenuPrincipal

        self.clear_frame()
        MenuPrincipal(self.root)
