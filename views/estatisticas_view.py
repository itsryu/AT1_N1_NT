import tkinter as tk
from tkinter import ttk
from controllers.estatisticas_controller import EstatisticasController

class EstatisticasView:
    def __init__(self, root):
        self.root = root
        self.controller = EstatisticasController()
        self.setup_ui()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        self.clear_frame()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(main_frame, text="Estatísticas e Relatórios", font=('Arial', 14), bg="#f0f0f0").pack(pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        tab1 = ttk.Frame(notebook)
        self.criar_aba_livros_categoria(tab1)
        notebook.add(tab1, text="Livros por Categoria")
        
        tab2 = ttk.Frame(notebook)
        self.criar_aba_emprestimos_tipo(tab2)
        notebook.add(tab2, text="Empréstimos por Tipo")
        
        tab3 = ttk.Frame(notebook)
        self.criar_aba_livros_mais_emprestados(tab3)
        notebook.add(tab3, text="Livros Mais Emprestados")
        
        tk.Button(main_frame, text="Voltar ao Menu", command=self.voltar_menu,
                 bg="#F44336", fg="white", width=20).pack(pady=10)

    def criar_aba_livros_categoria(self, parent):
        dados = self.controller.livros_por_categoria()
        
        frame = ttk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=('Categoria', 'Quantidade'), show='headings')
        tree.heading('Categoria', text='Categoria')
        tree.heading('Quantidade', text='Quantidade')
        tree.column('Categoria', width=200)
        tree.column('Quantidade', width=100)
        
        for categoria, qtd in dados.items():
            tree.insert('', 'end', values=(categoria, qtd))
        
        tree.pack(expand=True, fill='both')

    def criar_aba_emprestimos_tipo(self, parent):
        dados = self.controller.emprestimos_por_tipo_usuario()
        
        frame = ttk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=('Tipo de Usuário', 'Empréstimos'), show='headings')
        tree.heading('Tipo de Usuário', text='Tipo de Usuário')
        tree.heading('Empréstimos', text='Empréstimos')
        tree.column('Tipo de Usuário', width=200)
        tree.column('Empréstimos', width=100)
        
        for tipo, qtd in dados.items():
            tree.insert('', 'end', values=(tipo, qtd))
        
        tree.pack(expand=True, fill='both')

    def criar_aba_livros_mais_emprestados(self, parent):
        dados = self.controller.livros_mais_emprestados(limit=10)
        
        frame = ttk.Frame(parent)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=('Título', 'Autor', 'Categoria', 'Empréstimos'), show='headings')
        tree.heading('Título', text='Título')
        tree.heading('Autor', text='Autor')
        tree.heading('Categoria', text='Categoria')
        tree.heading('Empréstimos', text='Empréstimos')
        
        tree.column('Título', width=150)
        tree.column('Autor', width=120)
        tree.column('Categoria', width=120)
        tree.column('Empréstimos', width=80)
        
        for livro in dados:
            tree.insert('', 'end', values=(
                livro['titulo'],
                livro['autor'],
                livro['categoria'],
                livro['emprestimos']
            ))
        
        tree.pack(expand=True, fill='both')

    def voltar_menu(self):
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)