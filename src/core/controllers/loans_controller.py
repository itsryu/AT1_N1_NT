from typing import List
from datetime import datetime
from core.models.loan import Loan
from shared.file_manager import FileManager
from core.controllers.base_controller import BaseController
from shared.helpers import handle_errors

class LoansController(BaseController[Loan]):
    def __init__(self) -> None:
        super().__init__(FileManager(
            filename='data/loans.csv',
            headers=['ISBN', 'UserID', 'LoanDate', 'ReturnDate'],
            model_class=Loan
        ))

    @handle_errors
    def list_active(self) -> List[Loan]:
        return [loan for loan in self.list_all() if not loan.ReturnDate]

    @handle_errors
    def list_returned(self) -> List[Loan]:
        return [loan for loan in self.list_all() if loan.ReturnDate]

    @handle_errors
    def is_isbn_loaned(self, isbn: str | int) -> bool:
        isbn = str(isbn)
        return any(str(loan.ISBN) == isbn for loan in self.list_active())

    @handle_errors
    def register_loan(self, isbn: str | int, user_id: str) -> None:
        isbn = str(isbn)
        
        if self.is_isbn_loaned(isbn):
            raise ValueError("Este livro já está emprestado.")
        
        self.add(Loan(ISBN=str(isbn), UserID=user_id))

    @handle_errors
    def is_loan_late(self, isbn: str | int, user_id: str) -> bool:
        isbn = str(isbn)
        loans = self.list_all()

        loan = next((loan for loan in loans if str(loan.ISBN) == isbn and loan.UserID == user_id and not loan.ReturnDate), None)
        
        if loan:
            return (datetime.now() - loan.LoanDate).days > 30

        return False

    @handle_errors
    def register_return(self, isbn: str | int, user_id: str) -> bool:
        isbn = str(isbn)
        loans = self.list_all()

        loan = next((loan for loan in loans if str(loan.ISBN) == isbn and loan.UserID == user_id and not loan.ReturnDate), None)
        
        if loan:
            loan.ReturnDate = datetime.now()
            self.update_all(loans)
            return True

        return False
