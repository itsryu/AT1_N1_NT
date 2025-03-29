from typing import List, Optional
from datetime import datetime
from models.emprestimo import Emprestimo
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

class EmprestimosController(BaseController[Emprestimo]):
    def __init__(self):
        super().__init__(FileManager(
            filename='data/emprestimos.csv',
            headers=['ISBN', 'UserID', 'DataEmprestimo', 'DataDevolucao'],
            model_class=Emprestimo
        ))

    def listar_ativos(self) -> List[Emprestimo]:
        return [emp for emp in self.list_all() if not emp.DataDevolucao]
    
    def listar_devolvidos(self) -> List[Emprestimo]:
        return [emp for emp in self.list_all() if emp.DataDevolucao]
    
    def isbn_emprestado(self, isbn: str) -> bool:
        emprestimos = self.listar_ativos()
        return any(emp.ISBN == isbn for emp in emprestimos)
    
    def registrar_emprestimo(self, isbn: str, user_id: str) -> None:
        emprestimo = Emprestimo(ISBN=isbn, UserID=user_id)
        self.add(emprestimo)

    def registrar_devolucao(self, isbn: str, user_id: str) -> bool:
        emprestimos = self.list_all()
        updated = False
        
        for emp in emprestimos:
            if emp.ISBN == isbn and emp.UserID == user_id and not emp.DataDevolucao:
                emp.DataDevolucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break
        
        if updated:
            self.update_all(emprestimos)
        return updated