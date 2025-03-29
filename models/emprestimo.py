from datetime import datetime

class Emprestimo:
    def __init__(self, isbn, user_id, data_emprestimo=None, data_devolucao=None):
        self.isbn = isbn
        self.user_id = user_id
        self.data_emprestimo = data_emprestimo or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data_devolucao = data_devolucao

    def to_dict(self):
        return {
            'ISBN': self.isbn,
            'UserID': self.user_id,
            'DataEmprestimo': self.data_emprestimo,
            'DataDevolucao': self.data_devolucao or ''
        }