from typing import List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models.loan import Loan
from controllers.loans_controller import LoansController
from controllers.books_controller import BooksController
from controllers.users_controller import UsersController
from utils.helpers import handle_errors, format_date
from utils.logger import Logger
from utils.style import ColorPalette, Fonts
from views.base_view import BaseView
import datetime 


class LoansView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.controller = LoansController()
        self.books_controller = BooksController()
        self.users_controller = UsersController()

        self.clear_frame()
        self.setup_window()
        self.create_main_container()
        self.create_header_section()
        self.create_action_buttons()
        self.create_search_section()
        self.create_active_loans_section()
        self.create_returns_section()
        self.create_footer()
        self.load_data()

    @handle_errors
    def setup_window(self) -> None:
        self.root.title("Sistema de Empréstimos - Biblioteca Digital")
        self.center_window()

    @handle_errors
    def create_main_container(self) -> None:
        self.main_frame = self.create_frame(
            bg=ColorPalette.BACKGROUND,
            padx=20,
            pady=20
        )
        self.main_frame.pack(expand=True, fill=tk.BOTH)

    @handle_errors
    def create_header_section(self) -> None:
        header_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_frame = self.create_frame(header_frame, bg=ColorPalette.BACKGROUND)
        title_frame.pack(side=tk.LEFT, expand=True)
        
        self.create_label(
            title_frame,
            text="📚 Sistema de Empréstimos",
            font=Fonts.TITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        ).pack(anchor="w")

        self.create_button(
            header_frame,
            text="← Voltar ao Menu",
            command=self.back_to_menu,
            bg=ColorPalette.LIGHT,
            fg=ColorPalette.TEXT_PRIMARY,
            font=Fonts.BODY,
            width=15
        ).pack(side=tk.RIGHT)

    @handle_errors
    def create_action_buttons(self) -> None:
        btn_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND,
            pady=10
        )
        btn_frame.pack(fill=tk.X)

        buttons = [
            ("➕ Novo Empréstimo", self.new_loan, ColorPalette.PRIMARY),
            ("🔙 Registrar Devolução", self.register_return, ColorPalette.SUCCESS),
            ("🔄 Atualizar Listas", self.load_data, ColorPalette.INFO)
        ]

        for text, command, color in buttons:
            btn = self.create_button(
                btn_frame,
                text=text,
                command=command,
                bg=color,
                fg=ColorPalette.BUTTON_TEXT,
                font=Fonts.BUTTON,
                width=20
            )
            btn.pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_search_section(self) -> None:
        search_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.SURFACE,
            padx=15,
            pady=15,
            highlightbackground=ColorPalette.LIGHT,
            highlightthickness=1
        )
        search_frame.pack(fill=tk.X, pady=(0, 20))

        search_container = self.create_frame(search_frame, bg=ColorPalette.SURFACE)
        search_container.pack(fill=tk.X)

        self.search_entry = self.create_entry(
            search_container,
            font=Fonts.BODY,
            highlightcolor=ColorPalette.PRIMARY
        )
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        search_btn = self.create_button(
            search_container,
            text="🔍 Buscar",
            command=self.search_loans,
            bg=ColorPalette.INFO,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON
        )
        search_btn.pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_active_loans_section(self) -> None:
        section_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND
        )
        section_frame.pack(fill=tk.BOTH, expand=True)

        self.create_label(
            section_frame,
            text="📋 Empréstimos Ativos",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        ).pack(anchor=tk.W, pady=(0, 10))

        self.active_loans_tree = self.create_loans_treeview(section_frame)
        self.active_loans_tree.pack(expand=True, fill=tk.BOTH)

    @handle_errors
    def create_returns_section(self) -> None:
        section_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND
        )
        section_frame.pack(fill=tk.BOTH, expand=True)

        self.create_label(
            section_frame,
            text="📋 Histórico de Devoluções",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        ).pack(anchor=tk.W, pady=(0, 10))

        self.returns_tree = self.create_returns_treeview(section_frame)
        self.returns_tree.pack(expand=True, fill=tk.BOTH)

    @handle_errors
    def create_loans_treeview(self, parent: tk.Widget) -> ttk.Treeview:
        columns = [
            ("ID", 50, "center"),
            ("ISBN", 120, "center"),
            ("Título", 200, "w"),
            ("ID Usuário", 100, "center"),
            ("Usuário", 150, "w"),
            ("Data Empréstimo", 120, "center"),
            ("Status", 100, "center")
        ]

        tree = self.create_table(parent, columns)
        tree.bind("<Double-1>", lambda e: self.show_loan_details(self.active_loans_tree))
        return tree

    @handle_errors
    def create_returns_treeview(self, parent: tk.Widget) -> ttk.Treeview:
        columns = [
            ("ID", 50, "center"),
            ("ISBN", 120, "center"),
            ("Título", 200, "w"),
            ("ID Usuário", 100, "center"),
            ("Usuário", 150, "w"),
            ("Data Empréstimo", 120, "center"),
            ("Data Devolução", 120, "center")
        ]

        tree = self.create_table(parent, columns)
        tree.bind("<Double-1>", lambda e: self.show_loan_details(self.returns_tree))
        return tree

    @handle_errors
    def create_table(self, parent: tk.Widget, columns: List[Tuple[str, int, str]]) -> ttk.Treeview:
        tree = ttk.Treeview(
            parent,
            columns=[col[0] for col in columns],
            show="headings",
            selectmode="browse"
        )

        for col, width, anchor in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        style = ttk.Style()
        style.configure("Treeview", 
                      font=Fonts.BODY,
                      rowheight=25,
                      fieldbackground=ColorPalette.SURFACE)
        style.configure("Treeview.Heading", font=Fonts.BUTTON)
        style.map("Treeview", 
                background=[("selected", ColorPalette.PRIMARY)],
                foreground=[("selected", "white")])

        return tree

    @handle_errors
    def create_footer(self) -> None:
        footer_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND,
            pady=10
        )
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.create_label(
            footer_frame,
            text="Sistema de Biblioteca Digital © 2025",
            font=Fonts.FOOTER,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.BACKGROUND
        ).pack()

    @handle_errors
    def load_data(self) -> None:
        self.load_active_loans()
        self.load_returns()

    @handle_errors
    def load_active_loans(self) -> None:
        loans = self.controller.list_active()
        self.display_active_loans(loans)

    @handle_errors
    def load_returns(self) -> None:
        returns = self.controller.list_returned()
        self.display_returns(returns)

    @handle_errors
    def display_active_loans(self, loans: List[Loan]) -> None:
        self.active_loans_tree.delete(*self.active_loans_tree.get_children())
        
        books = {b.ISBN: b.Title for b in self.books_controller.list_all()}
        users = {u.ID: u.Name for u in self.users_controller.list_all()}

        for idx, loan in enumerate(loans, 1):
            self.active_loans_tree.insert(
                "", "end",
                values=(
                    idx,
                    loan.ISBN,
                    books.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    "Ativo" if not loan.ReturnDate else "Devolvido"
                ),
                tags=("late",) if self.is_late(loan) else ()
            )

        self.active_loans_tree.tag_configure("late", background=ColorPalette.DANGER)

    @handle_errors
    def is_late(self, loan: Loan) -> bool:
        if loan.ReturnDate:
            return False
        return datetime.datetime.now() > loan.LoanDate + datetime.timedelta(days=30)

    @handle_errors
    def display_returns(self, returns: List[Loan]) -> None:
        self.returns_tree.delete(*self.returns_tree.get_children())
        
        books = {b.ISBN: b.Title for b in self.books_controller.list_all()}
        users = {u.ID: u.Name for u in self.users_controller.list_all()}

        for idx, loan in enumerate(returns, 1):
            self.returns_tree.insert(
                "", "end",
                values=(
                    idx,
                    loan.ISBN,
                    books.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    format_date(loan.ReturnDate) if loan.ReturnDate else "N/A"
                )
            )

    @handle_errors
    def new_loan(self) -> None:
        isbn = self.get_input("Novo Empréstimo", "Digite o ISBN do livro:")
        if not isbn:
            return

        if not self.validate_book(isbn):
            return

        user_id = self.get_input("Novo Empréstimo", "Digite o ID do usuário:")
        if not user_id:
            return

        if not self.validate_user(user_id):
            return

        self.confirm_and_register_loan(isbn, user_id)

    @handle_errors
    def get_input(self, title: str, prompt: str) -> Optional[str]:
        value = simpledialog.askstring(title, prompt, parent=self.root)
        return value.strip() if value else None

    @handle_errors
    def validate_book(self, isbn: str) -> bool:
        try:
            if not self.books_controller.isbn_exists(isbn):
                self.show_error("ISBN não encontrado no sistema!")
                return False

            if self.controller.is_isbn_loaned(isbn):
                self.show_error("Livro já está emprestado!")
                return False

            return True
        except Exception as e:
            Logger.error(f"Erro ao validar livro: {str(e)}")
            self.show_error("Erro ao verificar livro!")
            return False
        
    @handle_errors
    def validate_user(self, user_id: str) -> bool:
        try:
            if not self.users_controller.id_exists(user_id):
                self.show_error("Usuário não encontrado!")
                return False
            return True
        except Exception as e:
            Logger.error(f"Erro ao validar usuário: {str(e)}")
            self.show_error("Erro ao verificar usuário!")
            return False
        
    @handle_errors
    def confirm_and_register_loan(self, isbn: str, user_id: str) -> None:
        book = self.books_controller.search_term(isbn)[0]
        user = next(u for u in self.users_controller.list_all() if u.ID == user_id)

        confirm = messagebox.askyesno(
            "Confirmar Empréstimo",
            f"Confirmar empréstimo do livro:\n\n"
            f"Título: {book.Title}\n"
            f"Para: {user.Name}\n\n"
            f"Deseja continuar?",
            icon="question"
        )

        if confirm:
            try:
                self.controller.register_loan(isbn, user_id)
                self.show_success("Empréstimo registrado com sucesso!")
                self.load_data()
            except Exception as e:
                Logger.error(f"Erro ao registrar empréstimo: {str(e)}")
                self.show_error("Erro ao registrar empréstimo!")

    @handle_errors
    def register_return(self) -> None:
        selected = self.active_loans_tree.selection()

        if not selected:
            self.show_warning("Selecione um empréstimo para devolver!")
            return

        item = self.active_loans_tree.item(selected[0])
        isbn = item["values"][1]
        user_id = item["values"][3]

        try:
            if self.controller.register_return(isbn, user_id):
                self.show_success("Devolução registrada com sucesso!")
                self.load_data()
            else:
                self.show_error("Não foi possível registrar a devolução!")
        except Exception as e:
            Logger.error(f"Erro ao registrar devolução: {str(e)}")
            self.show_error("Erro ao registrar devolução!")

    @handle_errors
    def search_loans(self) -> None:
        term = self.search_entry.get().strip().lower()
        if not term:
            self.load_active_loans()
            return

        loans = [
            loan for loan in self.controller.list_active()
            if term in loan.ISBN.lower() or term in loan.UserID.lower()
        ]
        self.display_active_loans(loans)

    @handle_errors
    def show_loan_details(self, tree: ttk.Treeview) -> None:
        selected = tree.selection()
        if not selected:
            return

        item = tree.item(selected[0])
        isbn = item["values"][1]
        user_id = item["values"][3]

        try:
            book = self.books_controller.search_term(isbn)[0]
            user = next(u for u in self.users_controller.list_all() if u.ID == user_id)
            loan = next(l for l in self.controller.list_all() 
                      if l.ISBN == isbn and l.UserID == user_id)

            details = (
                f"Livro:\n"
                f"Título: {book.Title}\n"
                f"ISBN: {book.ISBN}\n"
                f"Categoria: {book.Category}\n\n"
                f"Usuário:\n"
                f"Nome: {user.Name}\n"
                f"ID: {user.ID}\n"
                f"Tipo: {user.Type}\n\n"
                f"Empréstimo:\n"
                f"Data: {format_date(loan.LoanDate)}\n"
                f"Status: {'Devolvido' if loan.ReturnDate else 'Ativo'}\n"
            )

            if loan.ReturnDate:
                details += f"Data Devolução: {loan.ReturnDate.strftime("%d/%m/%Y %H:%M")}\n"

            messagebox.showinfo("Detalhes do Empréstimo", details)
        except Exception as e:
            Logger.error(f"Erro ao exibir detalhes: {str(e)}")
            self.show_error("Erro ao recuperar detalhes do empréstimo!")

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()
        MainMenu(self.root)