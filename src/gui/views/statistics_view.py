from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from core.controllers.statistics_controller import StatisticsController
from shared.components import PDFReport
from views.base_view import BaseView
from shared.helpers import handle_errors, format_date
from shared.style import ColorPalette, Fonts
from shared.components import Card, NativeBarChart, NativePieChart
from shared.logger import Logger

class StatisticsView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.controller = StatisticsController()
        self.summary_widgets: Dict[str, tk.Label] = {}
        self.limit_var = tk.IntVar(value=10)
        self.cards_frame = None
        self.clear_frame()
        self._setup_window()
        self._create_main_container()
        self._create_header()
        self._create_notebook()
        self._create_footer()
        self._load_data()

    def _setup_window(self) -> None:
        self.root.title("Estatísticas & Relatórios- Biblioteca Digital")
        self.center_window()

    def _create_main_container(self) -> None:
        self.main_frame = self.create_frame(bg=ColorPalette.BACKGROUND, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

    def _create_header(self) -> None:
        header_frame = self.create_frame(self.main_frame, bg=ColorPalette.BACKGROUND)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_frame = self.create_frame(header_frame, bg=ColorPalette.BACKGROUND)
        title_frame.pack(side=tk.LEFT, expand=True)
        self.create_label(title_frame, text="📊 Estatísticas & Relatórios", font=Fonts.TITLE, 
                         fg=ColorPalette.TEXT_PRIMARY, bg=ColorPalette.BACKGROUND).pack(anchor="w")

        btn_frame = self.create_frame(header_frame, bg=ColorPalette.BACKGROUND)
        btn_frame.pack(side=tk.RIGHT, padx=10)

        self._create_button(btn_frame, "📤 Exportar PDF", self._export_pdf, ColorPalette.SUCCESS)
        self._create_button(btn_frame, "← Voltar", self.back_to_menu, ColorPalette.LIGHT)

    def _create_button(self, parent: tk.Frame, text: str, command: callable, bg: str) -> None:
        self.create_button(parent, text=text, command=command, bg=bg,
                         fg=ColorPalette.BUTTON_TEXT if bg != ColorPalette.LIGHT else ColorPalette.TEXT_PRIMARY,
                         font=Fonts.BODY, width=15).pack(side=tk.RIGHT, padx=5)

    def _create_notebook(self) -> None:
        style = ttk.Style()
        style.configure("TNotebook", background=ColorPalette.BACKGROUND)
        style.configure("TNotebook.Tab", font=Fonts.BUTTON, padding=[10, 5],
                       background=ColorPalette.LIGHT, foreground=ColorPalette.TEXT_PRIMARY)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self._create_tabs()

    def _create_tabs(self) -> None:
        self._create_category_tab()
        self._create_user_type_tab()
        self._create_top_books_tab()
        self._create_summary_tab()

    def _create_category_tab(self) -> None:
        tab = self._create_tab("📚 Categorias")
        content_frame = self._create_content_frame(tab)

        self.category_tree = self._create_table(content_frame, [
            ("Categoria", 250, "w"), ("Quantidade", 150, "center"), ("Percentual", 150, "center")
        ])
        self.category_tree.pack(expand=True, fill=tk.BOTH)

        chart_frame = self._create_chart_frame(content_frame)
        data = self.controller.books_by_category()
        bar = NativeBarChart(data, "Livros por Categoria").create_tk_chart(chart_frame)
        bar.pack(expand=True, fill=tk.BOTH)

    def _create_user_type_tab(self) -> None:
        tab = self._create_tab("👥 Tipos de Usuário")
        content_frame = self._create_content_frame(tab)

        self.user_type_tree = self._create_table(content_frame, [
            ("Tipo", 250, "w"), ("Empréstimos", 150, "center"), ("Percentual", 150, "center")
        ])
        self.user_type_tree.pack(expand=True, fill=tk.BOTH)

        chart_frame = self._create_chart_frame(content_frame, pady=10)
        data = self.controller.loans_by_user_type()
        pie = NativePieChart(data, "Empréstimos por Tipo de Usuário").create_tk_chart(chart_frame)
        pie.pack(expand=True, fill=tk.BOTH)

    def _create_top_books_tab(self) -> None:
        tab = self._create_tab("🏆 Top Livros")
        content_frame = self._create_content_frame(tab)

        self.top_books_tree = self._create_table(content_frame, [
            ("Posição", 50, "center"), ("Título", 250, "w"), 
            ("ISBN", 150, "center"), ("Empréstimos", 100, "center"), ("Categoria", 150, "w")
        ])
        self.top_books_tree.pack(expand=True, fill=tk.BOTH)

        self._create_books_controls(content_frame)

    def _create_summary_tab(self) -> None:
        tab = self._create_tab("📋 Resumo")
        content_frame = self._create_content_frame(tab)

        self._create_summary_cards(content_frame)
        self._create_details_section(content_frame)
        self.update_summary_data()

    def _create_tab(self, text: str) -> tk.Frame:
        tab = self.create_frame(self.notebook, bg=ColorPalette.BACKGROUND)
        self.notebook.add(tab, text=text)
        return tab

    def _create_content_frame(self, parent: tk.Widget) -> tk.Frame:
        return self.create_frame(parent, bg=ColorPalette.BACKGROUND, padx=10, pady=10)

    def _create_chart_frame(self, parent: tk.Widget, pady: int = 10) -> tk.Frame:
        frame = self.create_frame(parent, bg=ColorPalette.BACKGROUND)
        frame.pack(fill=tk.X, pady=pady)
        return frame

    def _create_table(self, parent: tk.Widget, columns: List[Tuple[str, int, str]]) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=[col[0] for col in columns], 
                        show="headings", selectmode="browse", style="Custom.Treeview")

        style = ttk.Style()
        style.configure("Custom.Treeview", font=Fonts.BODY, rowheight=25, 
                    fieldbackground=ColorPalette.SURFACE)
        style.configure("Custom.Treeview.Heading", font=Fonts.BUTTON, 
                    background=ColorPalette.LIGHT, foreground=ColorPalette.TEXT_PRIMARY)

        for col, width, anchor in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        tree.bind("<Button-3>", lambda e: self.show_context_menu(e, tree))
        
        return tree

    def _create_books_controls(self, parent: tk.Widget) -> None:
        control_frame = self.create_frame(parent, bg=ColorPalette.BACKGROUND)
        control_frame.pack(fill=tk.X, pady=10)

        self.create_label(control_frame, text="Quantidade:", font=Fonts.BODY,
                         fg=ColorPalette.TEXT_PRIMARY, bg=ColorPalette.BACKGROUND).pack(side=tk.LEFT, padx=5)

        ttk.Spinbox(control_frame, from_=5, to=50, increment=5, textvariable=self.limit_var,
                   width=5, font=Fonts.BODY).pack(side=tk.LEFT, padx=5)

        self.create_button(control_frame, text="Atualizar", command=self._update_top_books,
                         bg=ColorPalette.INFO, fg=ColorPalette.BUTTON_TEXT, font=Fonts.BODY).pack(side=tk.LEFT, padx=5)

    def _create_summary_cards(self, parent: tk.Widget) -> None:
        if self.cards_frame:
            self.cards_frame.destroy()

        self.cards_frame = self.create_frame(parent, bg=ColorPalette.BACKGROUND)
        self.cards_frame.pack(fill=tk.X, pady=10)

        for title, key, command in [
            ("📚 Livros", "total_books", self._show_books),
            ("👥 Usuários", "total_users", self._show_users),
            ("🔄 Ativos", "active_loans", self._show_active_loans),
            ("✅ Finalizados", "completed_loans", self._show_completed_loans),
            ("📈 Média", "avg_loans_per_user", None)
        ]:
            card = Card(
                parent=self.cards_frame,
                title=title,
                value="0",
                color=ColorPalette.PRIMARY,
                command=command
            )
            self.summary_widgets[key] = card.value_label

    def _create_details_section(self, parent: tk.Widget) -> None:
        self.details_frame = self.create_frame(parent, bg=ColorPalette.BACKGROUND)
        self.details_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        search_frame = self.create_frame(self.details_frame, bg=ColorPalette.BACKGROUND)
        search_frame.pack(fill=tk.X, pady=5)

        self.search_entry = ttk.Entry(search_frame, font=Fonts.BODY)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        ttk.Button(search_frame, text="Buscar", command=self._perform_search,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)

        self.details_tree = ttk.Treeview(self.details_frame, columns=("ID", "Detalhes"), 
                                       show="headings", style="Custom.Treeview")
        self.details_tree.pack(expand=True, fill=tk.BOTH)

    def _create_footer(self) -> None:
        footer_frame = self.create_frame(self.main_frame, bg=ColorPalette.BACKGROUND, pady=10)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.create_label(footer_frame, 
                        text="Biblioteca Digital - Sistema de Gerenciamento de Acervo Literário",
                        font=Fonts.FOOTER, fg=ColorPalette.TEXT_SECONDARY,
                        bg=ColorPalette.BACKGROUND).pack()

    def _load_data(self) -> None:
        self._load_table_data(self.category_tree, self.controller.books_by_category(), 
                            lambda x: (x[0], x[1], f"{(x[1]/sum(self.controller.books_by_category().values()))*100:.1f}%"))
        
        self._load_table_data(self.user_type_tree, self.controller.loans_by_user_type(),
                            lambda x: (x[0], x[1], f"{(x[1]/sum(self.controller.loans_by_user_type().values()))*100:.1f}%"))
        
        self._update_top_books()

    def _load_table_data(self, tree: ttk.Treeview, data: Dict[str, int], formatter: callable) -> None:
        tree.delete(*tree.get_children())
        for item in data.items():
            tree.insert("", "end", values=formatter(item))

    def _update_top_books(self) -> None:
        self._load_table_data(self.top_books_tree, 
                            dict(enumerate(self.controller.most_loaned_books(limit=self.limit_var.get()), 1)),
                            lambda x: (x[0], x[1][0], x[1][1], x[1][2], x[1][3]))

    def update_summary_data(self) -> None:
        stats = self.controller.get_summary_stats()
        for key, label in self.summary_widgets.items():
            value = stats.get(key, 0)
            label.config(text=f"{value:.1f}" if isinstance(value, float) else str(value))

    def _show_books(self) -> None:
        self._show_details("📚 Livros", 
                         [("ISBN", 150), ("Título", 300), ("Autor", 200), ("Categoria", 150)],
                         [(b.ISBN, b.Title, b.Author, b.Category) for b in self.controller.books.list_all()])

    def _show_users(self) -> None:
        self._show_details("👥 Usuários",
                         [("ID", 100), ("Nome", 250), ("Email", 250), ("Tipo", 100)],
                         [(u.ID, u.Name, u.Email, u.Type) for u in self.controller.users.list_all()])

    def _show_active_loans(self) -> None:
        loans = [loan for loan in self.controller.loans.list_all() if not loan.ReturnDate]
        books = {b.ISBN: b.Title for b in self.controller.books.list_all()}
        users = {u.ID: u.Name for u in self.controller.users.list_all()}
        
        self._show_details("🔄 Ativos",
                         [("ID", 50), ("Livro", 250), ("Usuário", 200), ("Data", 150)],
                         [(i+1, books.get(l.ISBN, "?"), users.get(l.UserID, "?"), format_date(l.LoanDate)) 
                          for i, l in enumerate(loans)])

    def _show_completed_loans(self) -> None:
        loans = [loan for loan in self.controller.loans.list_all() if loan.ReturnDate]
        books = {b.ISBN: b.Title for b in self.controller.books.list_all()}
        users = {u.ID: u.Name for u in self.controller.users.list_all()}
        
        self._show_details("✅ Finalizados",
                         [("ID", 50), ("Livro", 250), ("Usuário", 200), ("Empréstimo", 150), ("Devolução", 150)],
                         [(i+1, books.get(l.ISBN, "?"), users.get(l.UserID, "?"), 
                          format_date(l.LoanDate), format_date(l.ReturnDate)) 
                          for i, l in enumerate(loans)])

    def _show_details(self, title: str, columns: List[Tuple[str, int]], data: List[Tuple]) -> None:
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        search_frame = tk.Frame(self.details_frame, bg=ColorPalette.BACKGROUND)
        search_frame.pack(fill=tk.X, pady=5)
        
        self.search_entry = ttk.Entry(search_frame, font=Fonts.BODY)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        ttk.Button(search_frame, text="Buscar", command=self._perform_search,
                style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.details_frame, text=title, font=Fonts.SUBTITLE, 
                fg=ColorPalette.TEXT_PRIMARY, bg=ColorPalette.BACKGROUND).pack(anchor=tk.W)
        
        self.details_tree = ttk.Treeview(self.details_frame, columns=[col[0] for col in columns], 
                                    show="headings", style="Custom.Treeview", selectmode="browse")
        for col, width in columns:
            self.details_tree.heading(col, text=col)
            self.details_tree.column(col, width=width)
        
        vsb = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_tree.yview)
        hsb = ttk.Scrollbar(self.details_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.details_tree.pack(expand=True, fill=tk.BOTH)
        
        for item in data:
            self.details_tree.insert("", "end", values=item)
        
        self.details_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.details_tree))

    def _clear_details(self) -> None:
        self.details_tree.delete(*self.details_tree.get_children())

    def _perform_search(self) -> None:
        term = self.search_entry.get().strip().lower()
        if not term:
            return
        
        items = [self.details_tree.item(item)["values"] for item in self.details_tree.get_children()]
        filtered = [item for item in items if any(term in str(field).lower() for field in item)]
        
        self._clear_details()
        for item in filtered:
            self.details_tree.insert("", "end", values=item)

    @handle_errors
    def show_context_menu(self, event: tk.Event, tree: ttk.Treeview) -> None:
        """Exibe o menu de contexto para copiar valores específicos"""
        item = tree.identify_row(event.y)
        if not item:
            return
            
        tree.selection_set(item)
        menu = tk.Menu(self.root, tearoff=0)
        columns = tree["columns"]
        
        for i, col in enumerate(columns):
            menu.add_command(
                label=f"Copiar {tree.heading(col)['text']}",
                command=lambda idx=i: self.copy_value(tree, item, idx)
            )
        
        menu.add_separator()
        menu.add_command(label="Fechar", command=menu.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    @handle_errors
    def copy_value(self, tree: ttk.Treeview, item_id: str, col_index: int) -> None:
        value = tree.item(item_id)["values"][col_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(str(value))
        self.show_success(f"'{value}' copiado para a área de transferência")

    @handle_errors
    def _export_pdf(self) -> None:
        try:
            pdf = PDFReport(self.controller)
            report_path = pdf.generate()
            self.show_success(f"PDF gerado: {report_path}")
        except Exception as e:
            Logger.error(f"Error generating PDF: {e}")
            self.show_error(f"Erro ao gerar PDF: {str(e)}")

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()
        MainMenu(self.root)