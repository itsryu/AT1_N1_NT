from typing import Dict, List, Optional
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from controllers.users_controller import UsersController
from views.base_view import BaseView
from utils.helpers import handle_errors
from utils.logger import Logger
from utils.style import ColorPalette, Fonts


class UsersView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.controller = UsersController()
        self.user_type_var = tk.StringVar(value="Visitante")
        self.entries: Dict[str, tk.Widget] = {}
        self.tree: Optional[ttk.Treeview] = None

        self.clear_frame()
        self.setup_window()
        self.create_main_container()
        self.create_header_section()
        self.create_form_section()
        self.create_search_section()
        self.create_results_section()
        self.create_footer()
        self.load_users()

    @handle_errors
    def setup_window(self) -> None:
        self.root.title("Cadastro de Usuários - Biblioteca Digital")
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
            text="👥 Cadastro de Usuários",
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
            text="Novo Usuário",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.SURFACE
        ).pack(anchor=tk.W, pady=(0, 10))

        self.entries = self.create_form_fields(form_frame)
        self.create_form_buttons(form_frame)

    @handle_errors
    def create_form_fields(self, parent: tk.Widget) -> Dict[str, tk.Widget]:
        fields = [
            ("Nome", "Digite o nome completo", "entry"),
            ("Email", "exemplo@email.com", "entry"),
            ("ID", "Número de identificação", "entry"),
            ("Tipo", "", "combobox")
        ]
        
        entries = {}
        
        for field, placeholder, field_type in fields:
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

            if field_type == "entry":
                entry = self.create_entry(
                    row_frame,
                    font=Fonts.BODY,
                    highlightcolor=ColorPalette.PRIMARY,
                    highlightthickness=1
                )
                entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
                self.setup_placeholder(entry, placeholder)
                entries[field] = entry
                
            elif field_type == "combobox":
                combo = ttk.Combobox(
                    row_frame,
                    textvariable=self.user_type_var,
                    values=list(User.ALLOWED_TYPES),
                    font=Fonts.BODY,
                    state="readonly"
                )
                combo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
                entries[field] = combo

        return entries

    @handle_errors
    def setup_placeholder(self, entry: tk.Entry, text: str) -> None:
        entry.insert(0, text)
        entry.config(fg=ColorPalette.GRAY)
        
        def on_focus_in(_):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg=ColorPalette.TEXT_PRIMARY)
        
        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=ColorPalette.GRAY)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    @handle_errors
    def create_form_buttons(self, parent: tk.Widget) -> None:
        btn_frame = self.create_frame(parent, bg=ColorPalette.SURFACE)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        buttons = [
            ("💾 Salvar Usuário", self.save_user, ColorPalette.SUCCESS),
            ("🧹 Limpar Campos", self.clear_fields, ColorPalette.WARNING)
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

        self.create_label(
            search_frame,
            text="Buscar Usuários",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.SURFACE
        ).pack(anchor=tk.W, pady=(0, 10))

        search_container = self.create_frame(search_frame, bg=ColorPalette.SURFACE)
        search_container.pack(fill=tk.X)

        self.entry_search = self.create_entry(
            search_container,
            font=Fonts.BODY,
            highlightcolor=ColorPalette.PRIMARY
        )
        self.entry_search.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        search_btn = self.create_button(
            search_container,
            text="🔍 Buscar",
            command=self.search_user,
            bg=ColorPalette.INFO,
            fg=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON
        )
        search_btn.pack(side=tk.LEFT, padx=5)

    @handle_errors
    def create_results_section(self) -> None:
        table_frame = self.create_frame(self.main_frame, bg=ColorPalette.BACKGROUND)
        table_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Nome", "Email", "ID", "Tipo"),
            show="headings",
            selectmode="browse"
        )

        columns = [
            ("Nome", 200, "w"),
            ("Email", 250, "w"),
            ("ID", 120, "center"),
            ("Tipo", 100, "center")
        ]

        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        style = ttk.Style()
        style.configure("Treeview", 
                      font=Fonts.BODY,
                      rowheight=25,
                      fieldbackground=ColorPalette.SURFACE)
        style.configure("Treeview.Heading", font=Fonts.BUTTON)
        style.map("Treeview", 
                background=[("selected", ColorPalette.PRIMARY)],
                foreground=[("selected", "white")])

        self.tree.bind("<Button-3>", self.show_context_menu)

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
    def show_context_menu(self, event: tk.Event) -> None:
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        self.tree.selection_set(item)
        
        menu = tk.Menu(self.root, tearoff=0)
        columns = ["Nome", "Email", "ID", "Tipo"]
        
        for i, col in enumerate(columns):
            menu.add_command(
                label=f"Copiar {col}",
                command=lambda idx=i: self.copy_value(item, idx)
            )
        
        menu.add_separator()
        
        menu.add_command(
            label="Excluir Usuário",
            command=lambda: self.confirm_and_delete_user(item)
        )
        
        menu.add_separator()
        menu.add_command(label="Fechar", command=menu.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    @handle_errors
    def copy_value(self, item_id: str, col_index: int) -> None:
        value = self.tree.item(item_id)["values"][col_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.show_success(f"'{value}' copiado para a área de transferência")

    @handle_errors
    def save_user(self) -> None:
        user_data = {
            "Name": self.get_entry_value("Nome"),
            "Email": self.get_entry_value("Email"),
            "ID": self.get_entry_value("ID"),
            "Type": self.user_type_var.get()
        }
        
        try:
            self.controller.register_user(user_data)
            self.show_success("Usuário cadastrado com sucesso!")
            self.load_users()
            self.clear_fields()
        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            Logger.error(f"Error saving user: {str(e)}")
            self.show_error("Erro ao salvar usuário")

    @handle_errors
    def confirm_and_delete_user(self, item_id: str) -> None:
        user_data = self.tree.item(item_id)["values"]
        user_id = user_data[2]
        
        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o usuário:\n\n"
            f"Nome: {user_data[0]}\n"
            f"ID: {user_data[2]}\n\n"
            f"Esta ação não pode ser desfeita.",
            icon="warning"
        )
        
        if confirm:
            try:
                self.controller.delete_user(user_id)
                self.show_success("Usuário excluído com sucesso!")
                self.load_users()
            except Exception as e:
                Logger.error(f"Error deleting user: {str(e)}")
                self.show_error("Erro ao excluir usuário")

    @handle_errors
    def get_entry_value(self, field: str) -> str:
        widget = self.entries[field]
        if isinstance(widget, tk.Entry):
            value = widget.get()
            placeholder = {
                "Nome": "Digite o nome completo",
                "Email": "exemplo@email.com",
                "ID": "Número de identificação"
            }.get(field, "")
            return "" if value == placeholder else value.strip()
        return ""

    @handle_errors
    def clear_fields(self) -> None:
        for field, widget in self.entries.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                placeholder = {
                    "Nome": "Digite o nome completo",
                    "Email": "exemplo@email.com",
                    "ID": "Número de identificação"
                }.get(field, "")
                if placeholder:
                    self.setup_placeholder(widget, placeholder)
        
        self.user_type_var.set("Visitante")

    @handle_errors
    def search_user(self) -> None:
        term = self.entry_search.get().strip()
        if not term:
            self.show_error("Digite um termo de busca")
            return
            
        try:
            results = self.controller.search_term(term)
            if not results:
                self.show_info("Nenhum usuário encontrado")
            self.show_results(results)
        except Exception as e:
            Logger.error(f"Error searching users: {str(e)}")
            self.show_error("Erro na busca de usuários")

    @handle_errors
    def load_users(self) -> None:
        try:
            users = self.controller.list_all()
            self.show_results(users)
        except Exception as e:
            Logger.error(f"Error loading users: {str(e)}")
            self.show_error("Erro ao carregar lista de usuários")

    @handle_errors
    def show_results(self, users: List[User]) -> None:
        self.tree.delete(*self.tree.get_children())
        
        for user in users:
            self.tree.insert("", tk.END, values=(
                user.Name,
                user.Email,
                user.ID,
                user.Type
            ))

    @handle_errors
    def back_to_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()
        MainMenu(self.root)