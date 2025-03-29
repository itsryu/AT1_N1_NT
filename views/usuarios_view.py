from tkinter import ttk, StringVar
from typing import Dict, List
from models.usuario import Usuario
from controllers.usuarios_controller import UsuariosController
from views.base_view import BaseView
import tkinter as tk

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].show_error(f"Ocorreu um erro em '{func.__name__}': {e}")
    return wrapper

class UsuariosView(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        self.clear_frame()
        self.controller = UsuariosController()
        self.tipo_var = StringVar(value="Aluno")

        main_frame = self.create_frame(bg="#f0f0f0")
        self.setup_cadastro_section(main_frame)
        self.setup_busca_section(main_frame)
        self.setup_results_section(main_frame)
        self.setup_back_button(main_frame)
        self.carregar_usuarios()

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
            "Tipo": {"type": "combobox", "values": list(Usuario.TIPOS_PERMITIDOS), "var": self.tipo_var},
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

        self.create_button(btn_frame, "Salvar Usuário", self.salvar_usuario, bg="#4CAF50").pack(side="left", padx=5)
        self.create_button(btn_frame, "Limpar", self.limpar_campos, bg="#607D8B").pack(side="left", padx=5)

    @handle_errors
    def setup_busca_section(self, parent: tk.Widget) -> None:
        frame_busca = self.create_frame(parent, bg="#f0f0f0")

        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()

        self.create_label(search_frame, "Buscar:").pack(side="left", padx=5)
        self.entry_busca = self.create_entry(search_frame)
        self.entry_busca.pack(side="left", padx=5)

        self.create_button(search_frame, "Buscar", self.buscar_usuarios, bg="#4CAF50", width=10).pack(side="left", padx=5)

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
            menu.add_command(label="Copiar Nome", command=lambda: self.copiar_valor(iid, 0))
            menu.add_command(label="Copiar Email", command=lambda: self.copiar_valor(iid, 1))
            menu.add_command(label="Copiar ID", command=lambda: self.copiar_valor(iid, 2))
            menu.add_command(label="Copiar Tipo", command=lambda: self.copiar_valor(iid, 3))
            menu.add_separator()
            menu.add_command(label="Fechar", command=menu.unpost)
            menu.post(event.x_root, event.y_root)

    def copiar_valor(self, item_id: str, col_index: int) -> None:
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
        self.create_button(parent, "Voltar ao Menu", self.voltar_menu, bg="#F44336", width=20).pack(pady=10)

    @handle_errors
    def salvar_usuario(self) -> None:
        usuario_data = {
            "Nome": self.entries["Nome"].get().strip(),
            "Email": self.entries["Email"].get().strip(),
            "ID": self.entries["ID"].get().strip(),
            "Tipo": self.tipo_var.get(),
        }

        try:
            self.controller.cadastrar_usuario(usuario_data)
            self.show_success("Usuário cadastrado com sucesso!")
            self.carregar_usuarios()
            self.limpar_campos()
        except ValueError as e:
            self.show_error(str(e))

    @handle_errors
    def limpar_campos(self) -> None:
        for widget in self.entries.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")
        self.tipo_var.set("Aluno")

    @handle_errors
    def buscar_usuarios(self) -> None:
        termo = self.entry_busca.get().strip().lower()

        if not termo:
            self.carregar_usuarios()
            return

        resultados = [
            usuario for usuario in self.controller.list_all()
            if (termo in usuario.Nome.lower() or termo in usuario.Email.lower() or termo in usuario.Tipo.lower())
        ]

        self.mostrar_resultados(resultados)

    @handle_errors
    def carregar_usuarios(self) -> None:
        usuarios = self.controller.list_all()
        self.mostrar_resultados(usuarios)

    @handle_errors
    def mostrar_resultados(self, usuarios: List[Usuario]) -> None:
        self.tree.delete(*self.tree.get_children())
        
        for usuario in usuarios:
            self.tree.insert(
                "",
                "end",
                values=(
                    usuario.Nome,
                    usuario.Email,
                    usuario.ID,
                    usuario.Tipo.capitalize(),
                ),
            )

    @handle_errors
    def voltar_menu(self) -> None:
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)