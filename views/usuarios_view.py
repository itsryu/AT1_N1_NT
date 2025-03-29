import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuarios_controller import UsuariosController

class UsuariosView:
    def __init__(self, root):
        self.root = root
        self.controller = UsuariosController()
        self.setup_ui()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        self.clear_frame()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        frame_cadastro = tk.Frame(main_frame, bg="#f0f0f0")
        frame_cadastro.pack(fill='x', pady=10)
        
        tk.Label(frame_cadastro, text="Cadastro de Usuários", font=('Arial', 14), bg="#f0f0f0").pack(pady=10)
        
        fields = ['Nome', 'Email', 'ID', 'Tipo']
        self.entries = {}
        
        for field in fields[:3]:
            row_frame = tk.Frame(frame_cadastro, bg="#f0f0f0")
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(row_frame, text=field, bg="#f0f0f0", width=10, anchor='e').pack(side='left', padx=5)
            entry = tk.Entry(row_frame, width=40)
            entry.pack(side='left', padx=5)
            self.entries[field] = entry
        
        row_frame = tk.Frame(frame_cadastro, bg="#f0f0f0")
        row_frame.pack(fill='x', pady=5)
        
        tk.Label(row_frame, text="Tipo", bg="#f0f0f0", width=10, anchor='e').pack(side='left', padx=5)
        self.tipo_var = tk.StringVar()
        cb_tipo = ttk.Combobox(row_frame, textvariable=self.tipo_var, 
                              values=['aluno', 'professor', 'visitante'], width=37)
        cb_tipo.pack(side='left', padx=5)
        self.entries['Tipo'] = cb_tipo
        
        btn_frame = tk.Frame(frame_cadastro, bg="#f0f0f0")
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="Salvar Usuário", command=self.salvar_usuario, 
                 bg="#2196F3", fg="white", width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.limpar_campos,
                 bg="#607D8B", fg="white", width=15).pack(side='left', padx=5)
        
        frame_busca = tk.Frame(main_frame, bg="#f0f0f0")
        frame_busca.pack(fill='x', pady=10)
        
        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()
        
        tk.Label(search_frame, text="Buscar:", bg="#f0f0f0").pack(side='left', padx=5)
        self.entry_busca = tk.Entry(search_frame, width=40)
        self.entry_busca.pack(side='left', padx=5)
        tk.Button(search_frame, text="Buscar", command=self.buscar_usuarios,
                 bg="#4CAF50", fg="white").pack(side='left', padx=5)
        
        self.tree = ttk.Treeview(main_frame, columns=fields, show='headings', selectmode='browse')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for field in fields:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=120)
        
        tk.Button(main_frame, text="Voltar ao Menu", command=self.voltar_menu,
                 bg="#F44336", fg="white", width=20).pack(pady=10)
        
        self.carregar_usuarios()

    def salvar_usuario(self):
        usuario_data = {
            'Nome': self.entries['Nome'].get(),
            'Email': self.entries['Email'].get(),
            'id_usuario': self.entries['ID'].get(),
            'tipo': self.tipo_var.get()
        }
        
        try:
            self.controller.cadastrar_usuario(usuario_data)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.carregar_usuarios()
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
        self.tipo_var.set('')

    def buscar_usuarios(self):
        termo = self.entry_busca.get()
        usuarios = self.controller.listar_usuarios()
        resultados = [u for u in usuarios if termo.lower() in ' '.join(u.values()).lower()]
        self.mostrar_resultados(resultados)

    def carregar_usuarios(self):
        usuarios = self.controller.listar_usuarios()
        self.mostrar_resultados(usuarios)

    def mostrar_resultados(self, usuarios):
        self.tree.delete(*self.tree.get_children())
        for usuario in usuarios:
            self.tree.insert('', 'end', values=[usuario[field] for field in self.entries.keys()])

    def voltar_menu(self):
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)