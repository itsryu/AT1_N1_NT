from typing import Dict, List
from models.book import Book
from controllers.books_controller import BooksController
from views.base_view import BaseView
from utils.helpers import handle_errors
import tkinter as tk

class BooksView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = BooksController()

        main_frame = self.create_frame(bg="#f0f0f0")

        self.setup_cadastro_section(main_frame)
        self.setup_busca_section(main_frame)
        self.setup_results_table(main_frame)
        self.setup_back_button(main_frame)
        self.load_books()

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
    def show_context_menu(self, event) -> None:
        iid = self.tree.identify_row(event.y)

        if iid:
            self.tree.selection_set(iid)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Copiar Título", command=lambda: self.copy_value(iid, 0))
            menu.add_command(label="Copiar Autor", command=lambda: self.copy_value(iid, 1))
            menu.add_command(label="Copiar Ano", command=lambda: self.copy_value(iid, 2))
            menu.add_command(label="Copiar ISBN", command=lambda: self.copy_value(iid, 3))
            menu.add_command(label="Copiar Categoria", command=lambda: self.copy_value(iid, 4))
            menu.add_separator()
            menu.add_command(label="Fechar", command=menu.unpost)
            menu.post(event.x_root, event.y_root)

    @handle_errors
    def copy_value(self, item_id: str, col_index: int) -> None:
        item = self.tree.item(item_id)
        
        if "values" in item:
            valor = item["values"][col_index]
            self.root.clipboard_clear()
            self.root.clipboard_append(valor)
            self.show_success(f"'{valor}' copiado para a área de transferência.")
        else:
            self.show_error("Nenhum valor encontrado para copiar.")

    @handle_errors
    def create_action_buttons(self, parent: tk.Widget) -> None:
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)

        self.create_button(btn_frame, "Salvar Livro", self.save_book, bg="#4CAF50").pack(side="left", padx=5)
        self.create_button(btn_frame, "Limpar", self.save_book, bg="#607D8B").pack(side="left", padx=5)

    @handle_errors
    def setup_busca_section(self, parent: tk.Widget) -> None:
        frame_busca = self.create_frame(parent, bg="#f0f0f0")

        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.entry_busca = self.create_entry(search_frame)
        self.entry_busca.pack(side="left", padx=5)

        self.create_button(search_frame, "Buscar", self.search_book, bg="#4CAF50", width=10).pack(side="left", padx=5)

    @handle_errors
    def setup_results_table(self, parent: tk.Widget) -> None:
        self.tree = self.create_treeview(parent, columns=["Título", "Autor", "Ano", "ISBN", "Categoria"])
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree.bind("<Button-3>", self.show_context_menu)


    @handle_errors
    def setup_back_button(self, parent: tk.Widget) -> None:
        self.create_button(parent, "Voltar ao Menu", self.back_menu, bg="#F44336").pack(pady=10)

    @handle_errors
    def save_book(self) -> None:
        book_data = {
            "Title": self.entries["Título"].get(),
            "Author": self.entries["Autor"].get(),
            "Year": self.entries["Ano"].get(),
            "ISBN": self.entries["ISBN"].get(),
            "Category": self.entries["Categoria"].get(),
        }
        
        try:
            self.controller.register_book(book_data)
            self.show_success("Livro cadastrado com sucesso!")
            self.load_books()
            self.clear_fields()
        except ValueError as e:
            self.show_error(str(e))

    @handle_errors
    def clear_fields(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, "end")

    @handle_errors
    def search_book(self) -> None:
        termo = self.entry_busca.get()
        resultados = self.controller.search_term(termo)
        self.show_results(resultados)

    @handle_errors
    def load_books(self) -> None:
        livros = self.controller.list_all()
        self.show_results(livros)

    @handle_errors
    def show_results(self, livros: List[Book]) -> None:
        self.tree.delete(*self.tree.get_children())
        
        for livro in livros:
            self.tree.insert(
                "",
                "end",
                values=[
                    livro.Title,
                    livro.Author,
                    livro.Year,
                    livro.ISBN,
                    livro.Category,
                ],
            )

    @handle_errors
    def back_menu(self) -> None:
        from views.main_menu import MainMenu

        self.clear_frame()
        MainMenu(self.root)
