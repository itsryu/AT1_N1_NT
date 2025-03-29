import tkinter as tk
from .livros_view import LivrosView
from .usuarios_view import UsuariosView
from .emprestimos_view import EmprestimosView
from .estatisticas_view import EstatisticasView

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca Digital")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(main_frame, text="Sistema de Biblioteca Digital", 
                font=('Arial', 16), bg="#f0f0f0").pack(pady=20)
        
        buttons = [
            ("Cadastro de Livros", "#4CAF50", lambda: LivrosView(self.root)),
            ("Cadastro de Usuários", "#2196F3", lambda: UsuariosView(self.root)),
            ("Sistema de Empréstimos", "#FF9800", lambda: EmprestimosView(self.root)),
            ("Estatísticas e Relatórios", "#9C27B0", lambda: EstatisticasView(self.root)),
            ("Sair", "#F44336", self.root.quit)
        ]
        
        for text, color, command in buttons:
            tk.Button(main_frame, text=text, command=command, 
                     bg=color, fg="white", width=30, height=2).pack(pady=10)