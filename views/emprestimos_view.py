import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.emprestimos_controller import EmprestimosController
from controllers.livros_controller import LivrosController
from controllers.usuarios_controller import UsuariosController
from datetime import datetime

class EmprestimosView:
    def __init__(self, root):
        self.root = root
        self.controller = EmprestimosController()
        self.livros_ctrl = LivrosController()
        self.usuarios_ctrl = UsuariosController()
        self.setup_ui()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_ui(self):
        self.clear_frame()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(main_frame, text="Sistema de Empréstimos", font=('Arial', 14), bg="#f0f0f0").pack(pady=10)
        
        frame_operacoes = tk.Frame(main_frame, bg="#f0f0f0")
        frame_operacoes.pack(fill='x', pady=10)
        
        tk.Button(frame_operacoes, text="Novo Empréstimo", command=self.novo_emprestimo,
                 bg="#FF9800", fg="white", width=20).pack(side='left', padx=5)
        tk.Button(frame_operacoes, text="Devolver Livro", command=self.devolver_livro,
                 bg="#FF9800", fg="white", width=20).pack(side='left', padx=5)
        
        columns = ['ISBN', 'UserID', 'DataEmprestimo', 'Título', 'Usuário']
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        tk.Button(main_frame, text="Voltar ao Menu", command=self.voltar_menu,
                 bg="#F44336", fg="white", width=20).pack(pady=10)
        
        self.carregar_emprestimos_ativos()

    def novo_emprestimo(self):
        isbn = simpledialog.askstring("Novo Empréstimo", "Digite o ISBN do livro:")
        if not isbn:
            return
            
        user_id = simpledialog.askstring("Novo Empréstimo", "Digite o ID do usuário:")
        if not user_id:
            return
        
        try:
            self.controller.realizar_emprestimo(isbn, user_id)
            messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
            self.carregar_emprestimos_ativos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def devolver_livro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para devolver")
            return
            
        item = self.tree.item(selected[0])
        isbn = item['values'][0]
        user_id = item['values'][1]
        data_emp = item['values'][2]
        
        try:
            self.controller.registrar_devolucao(isbn, user_id, data_emp)
            messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
            self.carregar_emprestimos_ativos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def carregar_emprestimos_ativos(self):
        emprestimos = self.controller.listar_emprestimos_ativos()
        livros = {l['ISBN']: l['Título'] for l in self.livros_ctrl.listar_livros()}
        usuarios = {u['ID']: u['Nome'] for u in self.usuarios_ctrl.listar_usuarios()}
        
        self.tree.delete(*self.tree.get_children())
        for emp in emprestimos:
            livro_titulo = livros.get(emp['ISBN'], 'Desconhecido')
            usuario_nome = usuarios.get(emp['UserID'], 'Desconhecido')
            self.tree.insert('', 'end', values=[
                emp['ISBN'],
                emp['UserID'],
                emp['DataEmprestimo'],
                livro_titulo,
                usuario_nome
            ])

    def voltar_menu(self):
        from views.menu_principal import MenuPrincipal
        self.clear_frame()
        MenuPrincipal(self.root)