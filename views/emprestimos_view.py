from typing import List, Optional, Any, Dict
from datetime import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models.emprestimo import Emprestimo
from controllers.emprestimos_controller import EmprestimosController
from controllers.livros_controller import LivrosController
from controllers.usuarios_controller import UsuariosController
from utils.helpers import formatar_data
from views.base_view import BaseView


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].show_error(f"Ocorreu um erro em '{func.__name__}': {e}")

    return wrapper


class EmprestimosView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = EmprestimosController()
        self.livros_controller = LivrosController()
        self.usuarios_controller = UsuariosController()

        main_frame = self.create_frame(bg="#f0f0f0")
        self.create_label(
            main_frame, "Sistema de Empréstimos", font=("Arial", 14, "bold")
        ).pack(pady=(0, 15))

        self.create_action_buttons(main_frame)
        self.setup_busca_section(main_frame)
        self.setup_results_table(main_frame)
        self.setup_devolucoes_table(main_frame)
        self.setup_back_button(main_frame)

        self.carregar_emprestimos()
        self.carregar_devolucoes()

    @handle_errors
    def create_action_buttons(self, parent: tk.Widget) -> None:
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)

        self.create_button(
            btn_frame, "Novo Empréstimo", self.novo_emprestimo, bg="#FF9800", width=20
        ).pack(side="left", padx=5)
        self.create_button(
            btn_frame,
            "Registrar Devolução",
            self.registrar_devolucao,
            bg="#FF9800",
            width=20,
        ).pack(side="left", padx=5)

    @handle_errors
    def setup_busca_section(self, parent: tk.Widget) -> None:
        frame_busca = self.create_frame(parent, bg="#f0f0f0")
        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.entry_busca = self.create_entry(search_frame)
        self.entry_busca.pack(side="left", padx=5)
        self.create_button(
            search_frame, "Buscar", self.buscar_emprestimos, bg="#4CAF50", width=10
        ).pack(side="left", padx=5)

    @handle_errors
    def setup_results_table(self, parent: tk.Widget) -> None:
        label = self.create_label(parent, "Empréstimos Ativos", font=("Arial", 12, "bold"))
        label.pack(pady=(20, 5))

        columns = [
            "ID",
            "ISBN",
            "Título",
            "ID do Usuário",
            "Usuário",
            "Data do Empréstimo",
            "Status",
        ]
        self.tree = self.create_treeview(parent, columns=columns)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        col_config: Dict[str, Dict[str, Any]] = {
            "ID": {"width": 50, "anchor": "center"},
            "ISBN": {"width": 120, "anchor": "center"},
            "Título": {"width": 200, "anchor": "w"},
            "ID do Usuário": {"width": 80, "anchor": "center"},
            "Usuário": {"width": 150, "anchor": "w"},
            "Data do Empréstimo": {"width": 150, "anchor": "center"},
            "Status": {"width": 100, "anchor": "center"},
        }

        for col, config in col_config.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **config)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    @handle_errors
    def setup_back_button(self, parent: tk.Widget) -> None:
        self.create_button(
            parent, "Voltar ao Menu", self.voltar_menu, bg="#F44336", width=20
        ).pack(pady=10)

    @handle_errors
    def novo_emprestimo(self) -> None:
        isbn: Optional[str] = self.obter_isbn_livro()

        if not isbn:
            return

        if not self.verificar_disponibilidade_livro(isbn):
            return

        user_id: Optional[str] = self.obter_id_usuario()

        if not user_id:
            return

        if not self.verificar_usuario(user_id):
            return

        self.confirmar_registro_emprestimo(isbn, user_id)

    def obter_isbn_livro(self) -> Optional[str]:
        isbn: Optional[str] = simpledialog.askstring(
            "Novo Empréstimo", "Digite o ISBN do livro:", parent=self.root
        )

        if isbn is None:
            self.show_warning("Operação cancelada pelo usuário")
            return None

        isbn = isbn.strip()

        if not isbn: 
            self.show_warning("Digite um ISBN válido!")
            return None

        return isbn

    def verificar_disponibilidade_livro(self, isbn: str) -> bool:
        try:
            if not self.livros_controller.isbn_existe(isbn):
                self.show_error("ISBN não encontrado no sistema!")
                return False

            if self.controller.isbn_emprestado(isbn):
                self.show_error("Livro já está emprestado!")
                return False

            return True
        except Exception as e:
            self.show_error(f"Erro ao verificar livro: {str(e)}")
            return False

    def obter_id_usuario(self) -> Optional[str]:
        user_id: Optional[str] = simpledialog.askstring(
            "Novo Empréstimo", "Digite o ID do usuário:", parent=self.root
        )

        if user_id is None:
            self.show_warning("Operação cancelada pelo usuário")
            return None
        
        if not user_id.strip():
            self.show_warning("Digite um ID de usuário válido!")
            return None
        
        return user_id.strip()

    def verificar_usuario(self, user_id: str) -> bool:
        try:
            if not self.usuarios_controller.id_existe(user_id):
                self.show_error("Usuário não encontrado!")
                return False
            return True
        except Exception as e:
            self.show_error(f"Erro ao verificar usuário: {str(e)}")
            return False

    def confirmar_registro_emprestimo(self, isbn: str, user_id: str) -> None:
        livros = self.livros_controller.buscar_por_termo(isbn)

        if not livros:
            self.show_error("Livro não encontrado!")
            return

        livro = livros[0]

        usuarios = [u for u in self.usuarios_controller.list_all() if u.ID == user_id]

        if not usuarios:
            self.show_error("Usuário não encontrado!")
            return

        usuario = usuarios[0]

        confirmacao: bool = messagebox.askyesno(
            "Confirmar Empréstimo",
            f"Confirmar empréstimo do livro:\nTítulo: {livro.Título}\nPara usuário: {usuario.Nome}\n\nDeseja continuar?",
        )

        if confirmacao:
            try:
                self.controller.registrar_emprestimo(isbn, user_id)
                self.show_success("Empréstimo registrado com sucesso!")
                self.carregar_emprestimos()
            except Exception as e:
                self.show_error(f"Erro ao registrar empréstimo: {str(e)}")

    @handle_errors
    def registrar_devolucao(self) -> None:
        selected = self.tree.selection()

        if not selected:
            self.show_warning("Selecione um empréstimo para devolver!")
            return

        item = self.tree.item(selected[0])
        isbn = item["values"][1]
        user_id = item["values"][3]

        try:
            if self.controller.registrar_devolucao(isbn, user_id):
                self.show_success("Devolução registrada com sucesso!")
                self.carregar_emprestimos()
                self.carregar_devolucoes()
            else:
                self.show_error("Não foi possível registrar a devolução!")
        except Exception as e:
            self.show_error(f"Erro ao registrar devolução: {str(e)}")

    @handle_errors
    def buscar_emprestimos(self) -> None:
        termo: str = self.entry_busca.get().strip().lower()
        if not termo:
            self.carregar_emprestimos()
            return
        emprestimos: List[Emprestimo] = [
            emp
            for emp in self.controller.listar_ativos()
            if termo in emp.ISBN.lower() or termo in emp.UserID.lower()
        ]
        self.mostrar_resultados(emprestimos)

    @handle_errors
    def carregar_emprestimos(self) -> None:
        emprestimos: List[Emprestimo] = self.controller.listar_ativos()
        self.mostrar_resultados(emprestimos)

    @handle_errors
    def mostrar_resultados(self, emprestimos: List[Emprestimo]) -> None:
        self.tree.delete(*self.tree.get_children())
        livros: Dict[str, str] = {
            l.ISBN: l.Título for l in self.livros_controller.list_all()
        }
        usuarios: Dict[str, str] = {
            u.ID: u.Nome for u in self.usuarios_controller.list_all()
        }

        for idx, emp in enumerate(emprestimos, start=1):
            self.tree.insert(
                "",
                "end",
                values=(
                    idx,
                    emp.ISBN,
                    livros.get(emp.ISBN, "Desconhecido"),
                    emp.UserID,
                    usuarios.get(emp.UserID, "Desconhecido"),
                    formatar_data(emp.DataEmprestimo),
                    "Ativo" if not emp.DataDevolucao else "Devolvido",
                ),
            )

    @handle_errors
    def setup_devolucoes_table(self, parent: tk.Widget) -> None:
        label = self.create_label(parent, "Devoluções", font=("Arial", 12, "bold"))
        label.pack(pady=(20, 5))

        columns = [
            "ID",
            "ISBN",
            "Título",
            "ID do Usuário",
            "Usuário",
            "Data do Empréstimo",
            "Data da Devolução",
        ]
        self.tree_devolucoes = self.create_treeview(parent, columns=columns)
        self.tree_devolucoes.pack(expand=True, fill="both", padx=10, pady=10)

        col_config: Dict[str, Dict[str, Any]] = {
            "ID": {"width": 50, "anchor": "center"},
            "ISBN": {"width": 120, "anchor": "center"},
            "Título": {"width": 200, "anchor": "w"},
            "ID do Usuário": {"width": 80, "anchor": "center"},
            "Usuário": {"width": 150, "anchor": "w"},
            "Data do Empréstimo": {"width": 150, "anchor": "center"},
            "Data da Devolução": {"width": 150, "anchor": "center"},
        }

        for col, config in col_config.items():
            self.tree_devolucoes.heading(col, text=col)
            self.tree_devolucoes.column(col, **config)

        scrollbar = ttk.Scrollbar(
            parent, orient="vertical", command=self.tree_devolucoes.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree_devolucoes.configure(yscrollcommand=scrollbar.set)

    @handle_errors
    def carregar_devolucoes(self) -> None:
        devolucoes: List[Emprestimo] = self.controller.listar_devolvidos()
        self.mostrar_devolucoes(devolucoes)

    @handle_errors
    def mostrar_devolucoes(self, devolucoes: List[Emprestimo]) -> None:
        self.tree_devolucoes.delete(*self.tree_devolucoes.get_children())

        livros: Dict[str, str] = {
            l.ISBN: l.Título for l in self.livros_controller.list_all()
        }
        usuarios: Dict[str, str] = {
            u.ID: u.Nome for u in self.usuarios_controller.list_all()
        }

        for idx, emp in enumerate(devolucoes, start=1):
            self.tree_devolucoes.insert(
                "",
                "end",
                values=(
                    idx,
                    emp.ISBN,
                    livros.get(emp.ISBN, "Desconhecido"),
                    emp.UserID,
                    usuarios.get(emp.UserID, "Desconhecido"),
                    formatar_data(emp.DataEmprestimo),
                    formatar_data(emp.DataDevolucao) if emp.DataDevolucao else "N/A",
                ),
            )

    @handle_errors
    def voltar_menu(self) -> None:
        from views.menu_principal import MenuPrincipal

        self.clear_frame()
        MenuPrincipal(self.root)
