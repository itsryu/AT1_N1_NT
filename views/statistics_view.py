from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk
from controllers.statistics_controller import StatisticsController
from views.base_view import BaseView
from utils.helpers import handle_errors, format_date
from utils.style import ColorPalette, Fonts
from utils.logger import Logger
from datetime import datetime
import math


class StatisticsView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.controller = StatisticsController()

        self.clear_frame()
        self.setup_window()
        self.create_main_container()
        self.create_header_section()
        self.create_notebook()
        self.create_footer()
        self.load_data()

    @handle_errors
    def setup_window(self) -> None:
        self.root.title("Estatísticas - Biblioteca Digital")
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
            text="📊 Estatísticas e Relatórios",
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
    def create_notebook(self) -> None:
        style = ttk.Style()
        style.configure("TNotebook", background=ColorPalette.BACKGROUND)
        style.configure("TNotebook.Tab", 
                      font=Fonts.BUTTON,
                      padding=[10, 5],
                      background=ColorPalette.LIGHT,
                      foreground=ColorPalette.TEXT_PRIMARY)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.create_books_by_category_tab()
        self.create_loans_by_user_type_tab()
        self.create_most_loaned_books_tab()
        self.create_summary_tab()

    @handle_errors
    def create_books_by_category_tab(self) -> None:
        tab = self.create_frame(self.notebook, bg=ColorPalette.BACKGROUND)
        self.notebook.add(tab, text="📚 Por Categoria")

        content_frame = self.create_frame(tab, bg=ColorPalette.BACKGROUND)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.category_tree = self.create_table(
            content_frame,
            columns=[
                ("Categoria", 250, "w"),
                ("Quantidade", 150, "center"),
                ("Percentual", 150, "center")
            ]
        )
        self.category_tree.pack(expand=True, fill=tk.BOTH)

        chart_frame = self.create_frame(content_frame, bg=ColorPalette.BACKGROUND)
        chart_frame.pack(fill=tk.X, pady=10)
        self.category_chart = self.create_frame(chart_frame, bg=ColorPalette.BACKGROUND)
        self.category_chart.pack(fill=tk.X)

    @handle_errors
    def create_loans_by_user_type_tab(self) -> None:
        tab = self.create_frame(self.notebook, bg=ColorPalette.BACKGROUND)
        self.notebook.add(tab, text="👥 Por Tipo de Usuário")

        content_frame = self.create_frame(tab, bg=ColorPalette.BACKGROUND)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.user_type_tree = self.create_table(
            content_frame,
            columns=[
                ("Tipo de Usuário", 250, "w"),
                ("Empréstimos", 150, "center"),
                ("Percentual", 150, "center")
            ]
        )
        self.user_type_tree.pack(expand=True, fill=tk.BOTH)

        self.user_type_chart = self.create_frame(content_frame, bg=ColorPalette.BACKGROUND)
        self.user_type_chart.pack(fill=tk.X, pady=10)

    @handle_errors
    def create_summary_tab(self) -> None:
        tab = self.create_frame(self.notebook, bg=ColorPalette.BACKGROUND)
        self.notebook.add(tab, text="📋 Resumo Geral")

        content_frame = self.create_frame(tab, bg=ColorPalette.BACKGROUND)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        cards_frame = self.create_frame(content_frame, bg=ColorPalette.BACKGROUND)
        cards_frame.pack(fill=tk.X, pady=10)

        self.summary_stats = [
            ("📚 Total Livros", "total_books", self.show_books),
            ("👥 Total Usuários", "total_users", self.show_users),
            ("🔄 Empréstimos Ativos", "active_loans", self.show_active_loans),
            ("✅ Empréstimos Finalizados", "completed_loans", self.show_completed_loans),
            ("📈 Média Empréstimos/Usuário", "avg_loans_per_user", None)
        ]
        
        self.summary_widgets = {}
        
        for title, key, command in self.summary_stats:
            card = self.create_frame(
                cards_frame,
                bg=ColorPalette.SURFACE,
                highlightbackground=ColorPalette.LIGHT,
                highlightthickness=1
            )
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, ipady=10)
            
            title_label = tk.Label(
                card,
                text=title,
                font=Fonts.BODY,
                fg=ColorPalette.TEXT_SECONDARY,
                bg=ColorPalette.SURFACE
            )
            title_label.pack()

            value_label = tk.Label(
                card,
                text="0",
                font=("Arial", 14, "bold"),
                fg=ColorPalette.PRIMARY,
                bg=ColorPalette.SURFACE,
                cursor="hand2" if command else ""
            )
            value_label.pack()
            
            if command:
                value_label.bind("<Button-1>", lambda e, cmd=command: cmd())
            
            self.summary_widgets[key] = value_label

        self.details_frame = self.create_frame(content_frame, bg=ColorPalette.BACKGROUND)
        self.details_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        search_control_frame = self.create_frame(self.details_frame, bg=ColorPalette.BACKGROUND)
        search_control_frame.pack(fill=tk.X, pady=5)

        self.search_entry = ttk.Entry(
            search_control_frame,
            font=Fonts.BODY
        )
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.search_button = ttk.Button(
            search_control_frame,
            text="Buscar",
            command=self.perform_search,
            style="Accent.TButton"
        )
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.details_tree = ttk.Treeview(
            self.details_frame,
            columns=("ID", "Detalhes"),
            show="headings",
            style="Custom.Treeview"
        )
        self.details_tree.pack(expand=True, fill=tk.BOTH)

        self.update_summary_data()

    @handle_errors
    def update_summary_data(self) -> None:
        try:
            stats = self.controller.get_summary_stats()
            
            for key, label in self.summary_widgets.items():
                value = stats.get(key, 0)
                
                if key == "avg_loans_per_user":
                    label.config(text=f"{value:.1f}")
                else:
                    label.config(text=str(value))
                    
        except Exception as e:
            Logger.error(f"Erro ao atualizar dados de resumo: {str(e)}")
            self.show_error("Erro ao carregar dados de resumo")

    @handle_errors
    def show_books(self) -> None:
        try:
            books = self.controller.books.list_all()
            self.display_details(
                columns=[("ISBN", 150), ("Título", 300), ("Autor", 200), ("Categoria", 150)],
                data=[(b.ISBN, b.Title, b.Author, b.Category) for b in books],
                title="📚 Todos os Livros"
            )
        except Exception as e:
            Logger.error(f"Erro ao carregar livros: {str(e)}")
            self.show_error("Erro ao carregar lista de livros")

    @handle_errors
    def show_users(self) -> None:
        try:
            users = self.controller.users.list_all()
            self.display_details(
                columns=[("ID", 100), ("Nome", 250), ("Email", 250), ("Tipo", 100)],
                data=[(u.ID, u.Name, u.Email, u.Type) for u in users],
                title="👥 Todos os Usuários"
            )
        except Exception as e:
            Logger.error(f"Erro ao carregar usuários: {str(e)}")
            self.show_error("Erro ao carregar lista de usuários")

    @handle_errors
    def show_active_loans(self) -> None:
        try:
            loans = [loan for loan in self.controller.loans.list_all() if not loan.ReturnDate]
            books = {b.ISBN: b.Title for b in self.controller.books.list_all()}
            users = {u.ID: u.Name for u in self.controller.users.list_all()}
            
            self.display_details(
                columns=[("ID", 50), ("Livro", 250), ("Usuário", 200), ("Data Empréstimo", 150)],
                data=[(i+1, books.get(l.ISBN, "Desconhecido"), users.get(l.UserID, "Desconhecido"), format_date(l.LoanDate)) 
                     for i, l in enumerate(loans)],
                title="🔄 Empréstimos Ativos"
            )
        except Exception as e:
            Logger.error(f"Erro ao carregar empréstimos ativos: {str(e)}")
            self.show_error("Erro ao carregar empréstimos ativos")

    @handle_errors
    def show_completed_loans(self) -> None:
        try:
            loans = [loan for loan in self.controller.loans.list_all() if loan.ReturnDate]
            books = {b.ISBN: b.Title for b in self.controller.books.list_all()}
            users = {u.ID: u.Name for u in self.controller.users.list_all()}
            
            self.display_details(
                columns=[("ID", 50), ("Livro", 250), ("Usuário", 200), ("Data Empréstimo", 150), ("Data Devolução", 150)],
                data=[(i+1, books.get(l.ISBN, "Desconhecido"), users.get(l.UserID, "Desconhecido"), 
                      format_date(l.LoanDate), format_date(l.ReturnDate)) 
                     for i, l in enumerate(loans)],
                title="✅ Empréstimos Finalizados"
            )
        except Exception as e:
            Logger.error(f"Erro ao carregar empréstimos finalizados: {str(e)}")
            self.show_error("Erro ao carregar empréstimos finalizados")

    @handle_errors
    def display_details(self, columns: List[Tuple[str, int]], data: List[Tuple], title: str) -> None:
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        self.details_tree["columns"] = [col[0] for col in columns]
        for col in self.details_tree["columns"]:
            self.details_tree.heading(col, text=col)
        
        for col, width in columns:
            self.details_tree.column(col, width=width)
        
        for item in data:
            self.details_tree.insert("", "end", values=item)
        
        for widget in self.details_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget["text"].startswith(("📚", "👥", "🔄", "✅")):
                widget.destroy()
        
        tk.Label(
            self.details_frame,
            text=title,
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        ).pack(anchor=tk.W)

    @handle_errors
    def perform_search(self) -> None:
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            return
        
        items = [self.details_tree.item(item)["values"] for item in self.details_tree.get_children()]
        
        filtered_items = [
            item for item in items
            if any(search_term in str(field).lower() for field in item)
        ]
        
        self.details_tree.delete(*self.details_tree.get_children())
        for item in filtered_items:
            self.details_tree.insert("", "end", values=item)

    @handle_errors
    def create_most_loaned_books_tab(self) -> None:
        tab = self.create_frame(self.notebook, bg=ColorPalette.BACKGROUND)
        self.notebook.add(tab, text="🏆 Mais Emprestados")

        content_frame = self.create_frame(tab, bg=ColorPalette.BACKGROUND)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.top_books_tree = self.create_table(
            content_frame,
            columns=[
                ("Posição", 50, "center"),
                ("Título", 250, "w"),
                ("ISBN", 150, "center"),
                ("Empréstimos", 100, "center"),
                ("Categoria", 150, "w")
            ]
        )
        self.top_books_tree.pack(expand=True, fill=tk.BOTH)

        control_frame = self.create_frame(content_frame, bg=ColorPalette.BACKGROUND)
        control_frame.pack(fill=tk.X, pady=10)

        self.create_label(
            control_frame,
            text="Quantidade:",
            font=Fonts.BODY,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        ).pack(side=tk.LEFT, padx=5)

        self.limit_var = tk.IntVar(value=10)
        limit_spin = ttk.Spinbox(
            control_frame,
            from_=5,
            to=50,
            increment=5,
            textvariable=self.limit_var,
            width=5,
            font=Fonts.BODY
        )
        limit_spin.pack(side=tk.LEFT, padx=5)

        self.create_button(
            control_frame,
            text="Atualizar",
            command=self.update_top_books,
            bg=ColorPalette.INFO,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BODY
        ).pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_table(self, parent: tk.Widget, columns: List[Tuple[str, int, str]]) -> ttk.Treeview:
        tree = ttk.Treeview(
            parent,
            columns=[col[0] for col in columns],
            show="headings",
            selectmode="none",
            style="Custom.Treeview"
        )

        style = ttk.Style()
        style.configure("Custom.Treeview", 
                      font=Fonts.BODY,
                      rowheight=25,
                      fieldbackground=ColorPalette.SURFACE)
        style.configure("Custom.Treeview.Heading", 
                      font=Fonts.BUTTON,
                      background=ColorPalette.LIGHT,
                      foreground=ColorPalette.TEXT_PRIMARY)

        for col, width, anchor in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

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
            text="Sistema de Biblioteca Digital © 2025 - Relatório gerado em: " + datetime.now().strftime("%d/%m/%Y %H:%M"),
            font=Fonts.FOOTER,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.BACKGROUND
        ).pack()

    @handle_errors
    def load_data(self) -> None:
        self.load_books_by_category()
        self.load_loans_by_user_type()
        self.load_most_loaned_books()

    @handle_errors
    def load_books_by_category(self) -> None:
        try:
            data = self.controller.books_by_category()
            total = sum(data.values())
            
            self.category_tree.delete(*self.category_tree.get_children())
            for category, count in data.items():
                percent = (count / total) * 100 if total > 0 else 0
                self.category_tree.insert("", "end", values=(
                    category, 
                    count,
                    f"{percent:.1f}%"
                ))
            
            self.create_bar_chart(self.category_chart, data, ColorPalette.PRIMARY)
            
        except Exception as e:
            Logger.error(f"Error loading books by category: {str(e)}")
            self.show_error("Erro ao carregar dados por categoria")

    @handle_errors
    def load_loans_by_user_type(self) -> None:
        try:
            data = self.controller.loans_by_user_type()
            total = sum(data.values())
            
            self.user_type_tree.delete(*self.user_type_tree.get_children())
            for user_type, count in data.items():
                percent = (count / total) * 100 if total > 0 else 0
                self.user_type_tree.insert("", "end", values=(
                    user_type,
                    count,
                    f"{percent:.1f}%"
                ))
            
            self.create_pie_chart(self.user_type_chart, data)
            
        except Exception as e:
            Logger.error(f"Error loading loans by user type: {str(e)}")
            self.show_error("Erro ao carregar dados por tipo de usuário")

    @handle_errors
    def load_most_loaned_books(self) -> None:
        try:
            limit = self.limit_var.get()
            data = self.controller.most_loaned_books(limit=limit)
            
            self.top_books_tree.delete(*self.top_books_tree.get_children())
            for idx, (title, isbn, count, category) in enumerate(data, 1):
                self.top_books_tree.insert("", "end", values=(
                    idx,
                    title,
                    isbn,
                    count,
                    category
                ))
                
        except Exception as e:
            Logger.error(f"Error loading most loaned books: {str(e)}")
            self.show_error("Erro ao carregar livros mais emprestados")

    @handle_errors
    def update_top_books(self) -> None:
        self.load_most_loaned_books()

    @handle_errors
    def create_bar_chart(self, parent: tk.Widget, data: Dict[str, int], color: str) -> None:
        for widget in parent.winfo_children():
            widget.destroy()
        
        max_value = max(data.values()) if data else 1
        
        for category, value in data.items():
            row_frame = self.create_frame(parent, bg=ColorPalette.BACKGROUND)
            row_frame.pack(fill=tk.X, pady=2)
            
            self.create_label(
                row_frame,
                text=category,
                font=Fonts.BODY,
                fg=ColorPalette.TEXT_PRIMARY,
                bg=ColorPalette.BACKGROUND,
                width=20,
                anchor="e"
            ).pack(side=tk.LEFT, padx=5)
            
            bar_length = int((value / max_value) * 300) if max_value > 0 else 0
            bar = tk.Frame(
                row_frame,
                bg=color,
                height=20,
                width=bar_length
            )
            bar.pack(side=tk.LEFT)
            
            self.create_label(
                row_frame,
                text=str(value),
                font=Fonts.BODY,
                fg=ColorPalette.TEXT_PRIMARY,
                bg=ColorPalette.BACKGROUND,
                width=10
            ).pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_pie_chart(self, parent: tk.Widget, data: Dict[str, int]) -> None:
        for widget in parent.winfo_children():
            widget.destroy()
        
        total = sum(data.values())
        if total == 0:
            self.create_label(
                parent,
                text="Nenhum dado disponível para exibir",
                font=Fonts.BODY,
                fg=ColorPalette.TEXT_SECONDARY,
                bg=ColorPalette.BACKGROUND
            ).pack()
            return
            
        colors = [
            ColorPalette.PRIMARY,
            ColorPalette.SUCCESS,
            ColorPalette.WARNING,
            ColorPalette.DANGER,
            ColorPalette.INFO
        ]
        
        canvas = tk.Canvas(
            parent,
            bg=ColorPalette.BACKGROUND,
            height=250,
            width=400,
            highlightthickness=0
        )
        canvas.pack()
        
        center_x, center_y, radius = 200, 125, 80 
        start_angle = 0
        
        if len(data) == 1:
            label, value = next(iter(data.items()))
            canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill=colors[0],
                outline=""
            )
            
            canvas.create_text(
                center_x,
                center_y + radius + 30,
                text=f"{label} (100.0%)",
                font=Fonts.BODY,
                fill=ColorPalette.TEXT_PRIMARY
            )
            return
        
        for i, (label, value) in enumerate(data.items()):
            angle = (value / total) * 360
            color = colors[i % len(colors)]
            
            canvas.create_arc(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                start=start_angle,
                extent=angle,
                fill=color,
                outline=""
            )
            
            mid_angle = start_angle + angle / 2
            mid_angle_rad = math.radians(mid_angle)
            text_x = center_x + (radius + 40) * math.cos(mid_angle_rad)
            text_y = center_y + (radius + 40) * math.sin(mid_angle_rad)
            percent = (value / total) * 100
            
            canvas.create_text(
                text_x,
                text_y,
                text=f"{label} ({percent:.1f}%)",
                font=Fonts.BODY,
                fill=ColorPalette.TEXT_PRIMARY
            )
            
            start_angle += angle

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()
        MainMenu(self.root)