from typing import Dict, List, Tuple
from collections import defaultdict
from controllers.books_controller import BooksController
from controllers.users_controller import UsersController
from controllers.loans_controller import LoansController

class StatisticsController:
    def __init__(self) -> None:
        self.books = BooksController()
        self.users = UsersController()
        self.loans = LoansController()

    def books_by_category(self) -> Dict[str, int]:
        categories: defaultdict[str, int] = defaultdict(int)

        for book in self.books.list_all():
            categories[book.Category] += 1

        return dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))

    def loans_by_user_type(self) -> Dict[str, int]:
        users: Dict[str, str] = {user.ID: user.Type for user in self.users.list_all()}
        types: defaultdict[str, int] = defaultdict(int)
        
        for loan in self.loans.list_all():
            user_type = users.get(loan.UserID, 'Visitante')
            types[user_type] += 1
            
        return dict(sorted(types.items(), key=lambda item: item[1], reverse=True))

    def most_loaned_books(self, limit: int = 10) -> List[Tuple[str, str, int]]:
        books: Dict[str, str] = {book.ISBN: book.Title for book in self.books.list_all()}
        counts: defaultdict[str, int] = defaultdict(int)
        
        for loan in self.loans.list_all():
            counts[loan.ISBN] += 1
        
        return sorted(
            [(books.get(isbn, 'Visitante'), isbn, count) 
             for isbn, count in counts.items()],
            key=lambda x: x[2], reverse=True
        )[:limit]