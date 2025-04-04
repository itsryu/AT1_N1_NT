from typing import Dict, List, Optional
import tkinter as tk
from tkinter import ttk, messagebox
from core.models.book import Book
from core.controllers.books_controller import BooksController
from views.base_view import BaseView
from shared.helpers import handle_errors
from shared.style import ColorPalette, Fonts
from shared.logger import Logger


class BooksView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.controller: BooksController = BooksController()
        self.entries: Dict[str, tk.Entry] = {}
        self.tree: Optional[ttk.Treeview] = None

        self.clear_frame()
        self.setup_window()
        self.create_main_container()
        self.create_header_section()
        self.create_form_section()
        self.create_search_section()
        self.create_results_table()
        self.create_footer()
        self.load_books()

    @handle_errors
    def setup_window(self) -> None:
        self.root.title("Gerenciamento de Livros - Biblioteca Digital")
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

        title_label = self.create_label(
            header_frame,
            text="📚 Gerenciamento de Livros",
            font=Fonts.TITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        )
        title_label.pack(side=tk.LEFT)

        back_btn = self.create_button(
            header_frame,
            text="← Voltar ao Menu",
            command=self.back_to_menu,
            bg=ColorPalette.LIGHT,
            fg=ColorPalette.TEXT_PRIMARY,
            font=Fonts.BODY
        )
        back_btn.pack(side=tk.RIGHT)

    @handle_errors
    def create_form_section(self) -> None:
        form_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.SURFACE,
            padx=15,
            pady=15,
            highlightbackground=ColorPalette.LIGHT,
            highlightthickness=1
        )
        form_frame.pack(fill=tk.X, pady=(0, 20))

        self.create_label(
            form_frame,
            text="Cadastrar Livro",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.SURFACE
        ).pack(anchor=tk.W, pady=(0, 10))

        self.entries = self.create_form_fields(form_frame)
        self.create_form_buttons(form_frame)

    @handle_errors
    def create_form_fields(self, parent: tk.Widget) -> Dict[str, tk.Entry]:
        fields = [
            ("Título", "Digite o título do livro"),
            ("Autor", "Nome do autor"),
            ("Ano", "Ano de publicação"),
            ("ISBN", "Código ISBN"),
            ("Categoria", "Gênero literário")
        ]
        
        entries = {}
        
        for field, placeholder in fields:
            row_frame = self.create_frame(parent, bg=ColorPalette.SURFACE)
            row_frame.pack(fill=tk.X, pady=5)

            self.create_label(
                row_frame,
                text=f"{field}:",
                font=Fonts.BODY,
                fg=ColorPalette.TEXT_PRIMARY,
                bg=ColorPalette.SURFACE,
                width=12,
                anchor="e"
            ).pack(side=tk.LEFT, padx=5)

            entry = self.create_entry(
                row_frame,
                font=Fonts.BODY,
                highlightcolor=ColorPalette.PRIMARY,
                highlightthickness=1
            )
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            self.setup_placeholder(entry, placeholder)
            entries[field] = entry

        return entries
    
    @handle_errors
    def setup_placeholder(self, entry: tk.Entry, text: str) -> None:
        entry.insert(0, text)
        entry.config(fg=ColorPalette.GRAY)
        
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg=ColorPalette.TEXT_PRIMARY)
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=ColorPalette.GRAY)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    @handle_errors
    def create_form_buttons(self, parent: tk.Widget) -> None:
        btn_frame = self.create_frame(parent, bg=ColorPalette.SURFACE)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        save_btn = self.create_button(
            btn_frame,
            text="💾 Salvar Livro",
            command=self.save_book,
            bg=ColorPalette.SUCCESS,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON,
            width=15
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = self.create_button(
            btn_frame,
            text="🧹 Limpar Campos",
            command=self.clear_fields,
            bg=ColorPalette.WARNING,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

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

        self.create_label(
            search_frame,
            text="Buscar Livros",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.SURFACE
        ).pack(anchor=tk.W, pady=(0, 10))

        search_container = self.create_frame(search_frame, bg=ColorPalette.SURFACE)
        search_container.pack(fill=tk.X)

        self.entry_busca = self.create_entry(
            search_container,
            font=Fonts.BODY,
            highlightcolor=ColorPalette.PRIMARY
        )
        self.entry_busca.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        search_btn = self.create_button(
            search_container,
            text="🔍 Buscar",
            command=self.search_book,
            bg=ColorPalette.INFO,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON
        )
        search_btn.pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_results_table(self) -> None:
        table_frame = self.create_frame(self.main_frame, bg=ColorPalette.BACKGROUND)
        table_frame.pack(expand=True, fill=tk.BOTH)

        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Título", "Autor", "Ano", "ISBN", "Categoria"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="browse"
        )

        columns = [
            ("Título", 250),
            ("Autor", 150),
            ("Ano", 80),
            ("ISBN", 120),
            ("Categoria", 150)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=50)

        self.tree.pack(expand=True, fill=tk.BOTH)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        self.tree.bind("<Button-3>", self.show_context_menu)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=Fonts.BODY)
        style.configure("Treeview.Heading", font=Fonts.BUTTON)
        style.map("Treeview", background=[("selected", ColorPalette.PRIMARY)])

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
            text="Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário",
            font=Fonts.FOOTER,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.BACKGROUND
        ).pack()

    @handle_errors
    def show_context_menu(self, event: tk.Event) -> None:
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        self.tree.selection_set(item)
        
        menu = tk.Menu(self.root, tearoff=0)
        columns = ["Título", "Autor", "Ano", "ISBN", "Categoria"]
        
        for i, col in enumerate(columns):
            menu.add_command(
                label=f"Copiar {col}",
                command=lambda idx=i: self.copy_value(item, idx)
            )
        
        menu.add_separator()
        
        menu.add_command(
            label="Excluir Livro",
            command=lambda: self.confirm_and_delete_book(item)
        )
        
        menu.add_separator()
        menu.add_command(label="Fechar", command=menu.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    @handle_errors
    def confirm_and_delete_book(self, item_id: str) -> None:
        book_data = self.tree.item(item_id)["values"]
        book_id = book_data[3]
        
        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o livro:\n\n"
            f"Título: {book_data[0]}\n"
            f"IBSN: {book_data[3]}\n\n"
            f"Esta ação não pode ser desfeita.",
            icon="warning"
        )
        
        if confirm:
            try:
                self.controller.delete_book(book_id)
                self.show_success("Livro excluído com sucesso!")
                self.load_books()
            except Exception as e:
                Logger.error(f"Error deleting book: {str(e)}")
                self.show_error("Erro ao excluir livro")

    @handle_errors
    def copy_value(self, item_id: str, col_index: int) -> None:
        value = self.tree.item(item_id)["values"][col_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.show_success(f"'{value}' copiado para a área de transferência")

    @handle_errors
    def save_book(self) -> None:
        book_data = {
            "Title": self.get_entry_value("Título"),
            "Author": self.get_entry_value("Autor"),
            "Year": self.get_entry_value("Ano"),
            "ISBN": self.get_entry_value("ISBN"),
            "Category": self.get_entry_value("Categoria"),
        }
        
        try:
            self.controller.register_book(book_data)
            self.show_success("Livro cadastrado com sucesso!")
            self.load_books()
            self.clear_fields()
        except ValueError as e:
            self.show_error(str(e))

    def get_entry_value(self, field: str) -> str:
        value = self.entries[field].get()
        placeholder = {
            "Título": "Digite o título do livro",
            "Autor": "Nome do autor",
            "Ano": "Ano de publicação",
            "ISBN": "Código ISBN",
            "Categoria": "Gênero literário"
        }.get(field, "")
        
        return "" if value == placeholder else value

    @handle_errors
    def clear_fields(self) -> None:
        for field, entry in self.entries.items():
            entry.delete(0, tk.END)
            self.setup_placeholder(entry, {
                "Título": "Digite o título do livro",
                "Autor": "Nome do autor",
                "Ano": "Ano de publicação",
                "ISBN": "Código ISBN",
                "Categoria": "Gênero literário"
            }[field])

    @handle_errors
    def search_book(self) -> None:
        term = self.entry_busca.get()
        results = self.controller.search_term(term)
        self.show_results(results)

    @handle_errors
    def load_books(self) -> None:
        try:
            books = self.controller.list_all()
            self.show_results(books)
        except Exception as e:
            Logger.error(f"Error loading books: {str(e)}")
            self.show_error("Erro ao carregar lista de livros")

    @handle_errors
    def show_results(self, books: List[Book]) -> None:
        self.tree.delete(*self.tree.get_children())
        
        for book in books:
            self.tree.insert("", tk.END, values=(
                book.Title,
                book.Author,
                book.Year,
                book.ISBN,
                book.Category
            ))

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()
        MainMenu(self.root)