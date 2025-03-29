import tkinter as tk
from tkinter import ttk, messagebox
from controllers.livros_controller import LivrosController

class LivrosView:
    def __init__(self, root):
        self.root = root
        self.controller = LivrosController()
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
        
        tk.Label(frame_cadastro, text="Cadastro de Livros", font=('Arial', 14), bg="#f0f0f0").pack(pady=10)
        
        fields = ['Título', 'Autor', 'Ano', 'ISBN', 'Categoria']
        self.entries = {}
        
        for field in fields:
            row_frame = tk.Frame(frame_cadastro, bg="#f0f0f0")
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(row_frame, text=field, bg="#f0f0f0", width=10, anchor='e').pack(side='left', padx=5)
            entry = tk.Entry(row_frame, width=40)
            entry.pack(side='left', padx=5)
            self.entries[field] = entry
        
        btn_frame = tk.Frame(frame_cadastro, bg="#f0f0f0")
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="Salvar Livro", command=self.salvar_livro, 
                 bg="#4CAF50", fg="white", width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.limpar_campos,
                 bg="#607D8B", fg="white", width=15).pack(side='left', padx=5)
        
        frame_busca = tk.Frame(main_frame, bg="#f0f0f0")
        frame_busca.pack(fill='x', pady=10)
        
        search_frame = tk.Frame(frame_busca, bg="#f0f0f0")
        search_frame.pack()
        
        tk.Label(search_frame, text="Buscar:", bg="#f0f0f0").pack(side='left', padx=5)
        self.entry_busca = tk.Entry(search_frame, width=40)
        self.entry_busca.pack(side='left', padx=5)
        tk.Button(search_frame, text="Buscar", command=self.buscar_livros,
                 bg="#2196F3", fg="white").pack(side='left', padx=5)
        
        self.tree = ttk.Treeview(main_frame, columns=fields, show='headings', selectmode='browse')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for field in fields:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=120)
        
        tk.Button(main_frame, text="Voltar ao Menu", command=self.voltar_menu,
                 bg="#F44336", fg="white", width=20).pack(pady=10)
        
        self.carregar_livros()

    def salvar_livro(self):
        livro_data = {field: self.entries[field].get() for field in self.entries}
        
        try:
            self.controller.cadastrar_livro(livro_data)
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            self.carregar_livros()
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def buscar_livros(self):
        termo = self.entry_busca.get()
        resultados = self.controller.buscar_livros(termo)
        self.mostrar_resultados(resultados)

    def carregar_livros(self):
        livros = self.controller.listar_livros()
        self.mostrar_resultados(livros)

    def mostrar_resultados(self, livros):
        self.tree.delete(*self.tree.get_children())
        for livro in livros:
            # Garante que estamos usando as mesmas chaves que o controller
            self.tree.insert('', 'end', values=[
                livro.get('Título', ''),
                livro.get('Autor', ''),
                livro.get('Ano', ''),
                livro.get('ISBN', ''),
                livro.get('Categoria', '')
            ])

    def voltar_menu(self):
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)