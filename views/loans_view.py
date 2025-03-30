from typing import List, Optional, Any, Dict
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models.loan import Loan
from controllers.loans_controller import LoansController
from controllers.books_controller import BooksController
from controllers.users_controller import UsersController
from utils.helpers import format_date
from utils.helpers import handle_errors
from views.base_view import BaseView

class LoansView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = LoansController()
        self.books_controller = BooksController()
        self.users_controller = UsersController()

        main_frame = self.create_frame(bg="#f0f0f0")

        self.create_label(main_frame, "Sistema de Empréstimos", font=("Arial", 14, "bold")).pack(pady=(0, 15))
        self.build_action_buttons(main_frame)
        self.initialize_search_section(main_frame)
        self.initialize_results_table(main_frame)
        self.initialize_returns_table(main_frame)
        self.initialize_back_button(main_frame)

        self.load_loans()
        self.load_returns()

    @handle_errors
    def build_action_buttons(self, parent: tk.Widget) -> None:
        button_frame = tk.Frame(parent, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=10)

        self.create_button(
            button_frame, "Novo Empréstimo", self.new_loan, bg="#FF9800", width=20
        ).pack(side="left", padx=5)
        self.create_button(
            button_frame,
            "Registrar Devolução",
            self.register_return,
            bg="#FF9800",
            width=20,
        ).pack(side="left", padx=5)

    @handle_errors
    def initialize_search_section(self, parent: tk.Widget) -> None:
        search_container = self.create_frame(parent, bg="#f0f0f0")
        search_frame = tk.Frame(search_container, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.search_entry = self.create_entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        self.create_button(
            search_frame, "Buscar", self.search_loans, bg="#4CAF50", width=10
        ).pack(side="left", padx=5)

    @handle_errors
    def initialize_results_table(self, parent: tk.Widget) -> None:
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
    def initialize_back_button(self, parent: tk.Widget) -> None:
        self.create_button(
            parent, "Voltar ao Menu", self.back_to_menu, bg="#F44336", width=20
        ).pack(pady=10)

    @handle_errors
    def new_loan(self) -> None:
        isbn: Optional[str] = self.get_book_isbn()

        if not isbn:
            return

        if not self.check_book_availability(isbn):
            return

        user_id: Optional[str] = self.get_user_id()

        if not user_id:
            return

        if not self.check_user(user_id):
            return

        self.confirm_loan_registration(isbn, user_id)

    def get_book_isbn(self) -> Optional[str]:
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

    def check_book_availability(self, isbn: str) -> bool:
        try:
            if not self.books_controller.isbn_exists(isbn):
                self.show_error("ISBN não encontrado no sistema!")
                return False

            if self.controller.is_isbn_loaned(isbn):
                self.show_error("Livro já está emprestado!")
                return False

            return True
        except Exception as e:
            self.show_error(f"Erro ao verificar livro: {str(e)}")
            return False

    def get_user_id(self) -> Optional[str]:
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

    def check_user(self, user_id: str) -> bool:
        try:
            if not self.users_controller.id_exists(user_id):
                self.show_error("Usuário não encontrado!")
                return False
            return True
        except Exception as e:
            self.show_error(f"Erro ao verificar usuário: {str(e)}")
            return False

    def confirm_loan_registration(self, isbn: str, user_id: str) -> None:
        books_list = self.books_controller.search_term(isbn)

        if not books_list:
            self.show_error("Livro não encontrado!")
            return

        book = books_list[0]

        users_list = [u for u in self.users_controller.list_all() if u.ID == user_id]

        if not users_list:
            self.show_error("Usuário não encontrado!")
            return

        user = users_list[0]

        confirmation: bool = messagebox.askyesno(
            "Confirmar Empréstimo",
            f"Confirmar empréstimo do livro:\nTítulo: {book.Title}\nPara usuário: {user.Name}\n\nDeseja continuar?",
        )

        if confirmation:
            try:
                self.controller.register_loan(isbn, user_id)
                self.show_success("Empréstimo registrado com sucesso!")
                self.load_loans()
            except Exception as e:
                self.show_error(f"Erro ao registrar empréstimo: {str(e)}")

    @handle_errors
    def register_return(self) -> None:
        selected = self.tree.selection()

        if not selected:
            self.show_warning("Selecione um empréstimo para devolver!")
            return

        item = self.tree.item(selected[0])
        isbn = item["values"][1]
        user_id = item["values"][3]

        try:
            if self.controller.register_return(isbn, user_id):
                self.show_success("Devolução registrada com sucesso!")
                self.load_loans()
                self.load_returns()
            else:
                self.show_error("Não foi possível registrar a devolução!")
        except Exception as e:
            self.show_error(f"Erro ao registrar devolução: {str(e)}")

    @handle_errors
    def search_loans(self) -> None:
        term: str = self.search_entry.get().strip().lower()
        if not term:
            self.load_loans()
            return
        loans: List[Loan] = [
            loan
            for loan in self.controller.list_active()
            if term in loan.ISBN.lower() or term in loan.UserID.lower()
        ]
        self.display_results(loans)

    @handle_errors
    def load_loans(self) -> None:
        loans: List[Loan] = self.controller.list_active()
        self.display_results(loans)

    @handle_errors
    def display_results(self, loans: List[Loan]) -> None:
        self.tree.delete(*self.tree.get_children())
        books_dict: Dict[str, str] = {
            b.ISBN: b.Title for b in self.books_controller.list_all()
        }
        users_dict: Dict[str, str] = {
            u.ID: u.Name for u in self.users_controller.list_all()
        }

        for idx, loan in enumerate(loans, start=1):
            self.tree.insert(
                "",
                "end",
                values=(
                    idx,
                    loan.ISBN,
                    books_dict.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users_dict.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    "Ativo" if not loan.ReturnDate else "Devolvido",
                ),
            )

    @handle_errors
    def initialize_returns_table(self, parent: tk.Widget) -> None:
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
        self.returns_tree = self.create_treeview(parent, columns=columns)
        self.returns_tree.pack(expand=True, fill="both", padx=10, pady=10)

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
            self.returns_tree.heading(col, text=col)
            self.returns_tree.column(col, **config)

        scrollbar = ttk.Scrollbar(
            parent, orient="vertical", command=self.returns_tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.returns_tree.configure(yscrollcommand=scrollbar.set)

    @handle_errors
    def load_returns(self) -> None:
        returns: List[Loan] = self.controller.list_returned()
        self.display_returns(returns)

    @handle_errors
    def display_returns(self, returns: List[Loan]) -> None:
        self.returns_tree.delete(*self.returns_tree.get_children())

        books_dict: Dict[str, str] = {
            b.ISBN: b.Title for b in self.books_controller.list_all()
        }
        users_dict: Dict[str, str] = {
            u.ID: u.Name for u in self.users_controller.list_all()
        }

        for idx, loan in enumerate(returns, start=1):
            self.returns_tree.insert(
                "",
                "end",
                values=(
                    idx,
                    loan.ISBN,
                    books_dict.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users_dict.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    format_date(loan.ReturnDate) if loan.ReturnDate else "N/A",
                ),
            )

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu

        self.clear_frame()
        MainMenu(self.root)