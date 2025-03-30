from tkinter import ttk, StringVar
from typing import Dict, List
from models.user import User
from controllers.users_controller import UsersController
from views.base_view import BaseView
from utils.helpers import handle_errors
import tkinter as tk

class UsersView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = UsersController()
        self.tipo_var = StringVar(value="Visitante")

        main_frame = self.create_frame(bg="#f0f0f0")
        self.setup_cadastro_section(main_frame)
        self.setup_busca_section(main_frame)
        self.setup_results_section(main_frame)
        self.setup_back_button(main_frame)
        self.load_users()

    @handle_errors
    def setup_cadastro_section(self, parent: tk.Widget) -> None:
        frame_cadastro = self.create_frame(parent, bg="#f0f0f0")
        self.create_label(frame_cadastro, "Cadastro de Usuários", font=("Arial", 14)).pack(pady=10)

        self.entries = self.create_form_fields(frame_cadastro)
        self.create_action_buttons(frame_cadastro)

    @handle_errors
    def create_form_fields(self, parent: tk.Widget) -> Dict[str, tk.Widget]:
        fields = {
            "Nome": {"type": "entry"},
            "Email": {"type": "entry"},
            "ID": {"type": "entry"},
            "Tipo": {"type": "combobox", "values": list(User.ALLOWED_TYPES), "var": self.tipo_var},
        }
        
        entries = {}

        for field, config in fields.items():
            row_frame = tk.Frame(parent, bg="#f0f0f0")
            row_frame.pack(fill="x", pady=5)

            self.create_label(row_frame, field, width=10, anchor="e").pack(side="left", padx=5)

            if config["type"] == "entry":
                entries[field] = self.create_entry(row_frame)
                entries[field].pack(side="left", padx=5)
            elif config["type"] == "combobox":
                entries[field] = self.create_combobox(row_frame, values=config["values"], textvariable=config["var"])
                entries[field].pack(side="left", padx=5)
                entries[field].state(["readonly"])

        return entries

    @handle_errors
    def create_action_buttons(self, parent: tk.Widget) -> None:
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)

        self.create_button(btn_frame, "Salvar Usuário", self.save_user, bg="#4CAF50").pack(side="left", padx=5)
        self.create_button(btn_frame, "Limpar", self.clear_fields, bg="#607D8B").pack(side="left", padx=5)

    @handle_errors
    def setup_busca_section(self, parent: tk.Widget) -> None:
        frame_busca = self.create_frame(parent, bg="#f0f0f0")

        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.entry_busca = self.create_entry(search_frame)
        self.entry_busca.pack(side="left", padx=5)

        self.create_button(search_frame, "Buscar", self.search_user, bg="#4CAF50", width=10).pack(side="left", padx=5)

    @handle_errors
    def setup_results_section(self, parent: tk.Widget) -> None:
        columns = ["Nome", "Email", "ID", "Tipo"]
        self.tree = self.create_treeview(parent, columns=columns)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree.column("Nome", width=180, anchor="w")
        self.tree.column("Email", width=200, anchor="w")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Tipo", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Button-3>", self.show_context_menu)

    @handle_errors
    def show_context_menu(self, event) -> None:
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Copiar Nome", command=lambda: self.copy_value(iid, 0))
            menu.add_command(label="Copiar Email", command=lambda: self.copy_value(iid, 1))
            menu.add_command(label="Copiar ID", command=lambda: self.copy_value(iid, 2))
            menu.add_command(label="Copiar Tipo", command=lambda: self.copy_value(iid, 3))
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
            self.show_success(f"Valor '{valor}' copiado para a área de transferência.")
        else:
            self.show_error("Nenhum valor encontrado para copiar.")

    @handle_errors
    def setup_back_button(self, parent: tk.Widget) -> None:
        self.create_button(parent, "Voltar ao Menu", self.back_menu, bg="#F44336", width=20).pack(pady=10)

    @handle_errors
    def save_user(self) -> None:
        usuario_data = {
            "Name": self.entries["Nome"].get().strip(),
            "Email": self.entries["Email"].get().strip(),
            "ID": self.entries["ID"].get().strip(),
            "Type": self.tipo_var.get(),
        }

        try:
            self.controller.register_user(usuario_data)
            self.show_success("Usuário cadastrado com sucesso!")
            self.load_users()
            self.clear_fields()
        except ValueError as e:
            self.show_error(str(e))

    @handle_errors
    def clear_fields(self) -> None:
        for widget in self.entries.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")
                
        self.tipo_var.set("Visitante")

    @handle_errors
    def search_user(self) -> None:
        term = self.entry_busca.get().strip()

        if term:
            usuarios = self.controller.search_term(term)
            self.show_results(usuarios)
        else:
            self.show_error("Digite um termo de busca.")

    @handle_errors
    def load_users(self) -> None:
        usuarios = self.controller.list_all()
        self.show_results(usuarios)

    @handle_errors
    def show_results(self, usuarios: List[User]) -> None:
        self.tree.delete(*self.tree.get_children())
        
        for usuario in usuarios:
            self.tree.insert(
                "",
                "end",
                values=(
                    usuario.Name,
                    usuario.Email,
                    usuario.ID,
                    usuario.Type
                ),
            )

    @handle_errors
    def back_menu(self) -> None:
        from views.main_menu import MainMenu
        self.clear_frame()

        MainMenu(self.root)