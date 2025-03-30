from typing import List
from datetime import datetime
from models.loan import Loan
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

class LoansController(BaseController[Loan]):
    def __init__(self) -> None:
        super().__init__(FileManager(
            filename='data/loans.csv',
            headers=['ISBN', 'UserID', 'LoanDate', 'ReturnDate'],
            model_class=Loan
        ))

    def list_active(self) -> List[Loan]:
        return [loan for loan in self.list_all() if not loan.ReturnDate]
    
    def list_returned(self) -> List[Loan]:
        return [loan for loan in self.list_all() if loan.ReturnDate]
    
    def is_isbn_loaned(self, isbn: str) -> bool:
        active_loans = self.list_active()
        return any(loan.ISBN == isbn for loan in active_loans)
    
    def register_loan(self, isbn: str, user_id: str) -> None:
        loan = Loan(ISBN=isbn, UserID=user_id)
        self.add(loan)

    def register_return(self, isbn: str, user_id: str) -> bool:
        loans = self.list_all()
        updated = False
        
        for loan in loans:
            if loan.ISBN == isbn and loan.UserID == user_id and not loan.ReturnDate:
                loan.ReturnDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break
        
        if updated:
            self.update_all(loans)
        return updated