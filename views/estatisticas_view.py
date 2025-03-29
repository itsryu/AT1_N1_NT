from tkinter import ttk
import tkinter as tk
from controllers.estatisticas_controller import EstatisticasController
from views.base_view import BaseView

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].show_error(f"Ocorreu um erro em '{func.__name__}': {e}")
    return wrapper

class EstatisticasView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = EstatisticasController()
        
        main_frame = self.create_frame(bg="#f0f0f0")
        self.create_label(main_frame, "Estatísticas e Relatórios", font=("Arial", 14)).pack(pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Aba 1: Livros por Categoria
        tab1 = self.create_frame(notebook, bg="#f0f0f0")
        self.criar_aba_livros_categoria(tab1)
        notebook.add(tab1, text="Livros por Categoria")
        
        # Aba 2: Empréstimos por Tipo
        tab2 = self.create_frame(notebook, bg="#f0f0f0")
        self.criar_aba_emprestimos_tipo(tab2)
        notebook.add(tab2, text="Empréstimos por Tipo")
        
        # Aba 3: Livros Mais Emprestados
        tab3 = self.create_frame(notebook, bg="#f0f0f0")
        self.criar_aba_livros_mais_emprestados(tab3)
        notebook.add(tab3, text="Livros Mais Emprestados")
        
        self.create_button(main_frame, "Voltar ao Menu", self.voltar_menu, bg="#F44336", width=20).pack(pady=10)

    @handle_errors
    def criar_aba_livros_categoria(self, parent: tk.Widget) -> None:
        dados = self.controller.livros_por_categoria()
        
        frame = self.create_frame(parent, bg="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        tree = self.create_treeview(frame, columns=["Categoria", "Quantidade"])
        tree.heading("Categoria", text="Categoria")
        tree.heading("Quantidade", text="Quantidade")
        tree.column("Categoria", width=200, anchor="w")
        tree.column("Quantidade", width=100, anchor="center")
        
        for categoria, qtd in dados.items():
            tree.insert("", "end", values=(categoria, qtd))
        
        tree.pack(expand=True, fill="both")

    @handle_errors
    def criar_aba_emprestimos_tipo(self, parent: tk.Widget) -> None:
        dados = self.controller.emprestimos_por_tipo()
        
        frame = self.create_frame(parent, bg="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        tree = self.create_treeview(frame, columns=["Tipo de Usuário", "Empréstimos"])
        tree.heading("Tipo de Usuário", text="Tipo de Usuário")
        tree.heading("Empréstimos", text="Empréstimos")
        tree.column("Tipo de Usuário", width=200, anchor="w")
        tree.column("Empréstimos", width=100, anchor="center")
        
        for tipo, qtd in dados.items():
            tree.insert("", "end", values=(tipo, qtd))
        
        tree.pack(expand=True, fill="both")

    @handle_errors
    def criar_aba_livros_mais_emprestados(self, parent: tk.Widget) -> None:
        dados = self.controller.livros_mais_emprestados(limit=10)
        
        frame = self.create_frame(parent, bg="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        tree = self.create_treeview(frame, columns=["Título", "ISBN", "Empréstimos"])
        tree.heading("Título", text="Título")
        tree.heading("ISBN", text="ISBN")
        tree.heading("Empréstimos", text="Empréstimos")
        tree.column("Título", width=200, anchor="w")
        tree.column("ISBN", width=150, anchor="w")
        tree.column("Empréstimos", width=100, anchor="center")
        
        for livro in dados:
            tree.insert("", "end", values=(livro[0], livro[1], livro[2]))
        
        tree.pack(expand=True, fill="both")

    @handle_errors
    def voltar_menu(self) -> None:
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)