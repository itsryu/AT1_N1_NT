from typing import Dict, List, Tuple, DefaultDict, Any
from collections import defaultdict
from datetime import datetime, timedelta
from core.controllers.books_controller import BooksController
from core.controllers.users_controller import UsersController
from core.controllers.loans_controller import LoansController
from core.models.loan import Loan

class StatisticsController:
    def __init__(self) -> None:
        self.books = BooksController()
        self.users = UsersController()
        self.loans = LoansController()

    def books_by_category(self) -> Dict[str, int]:
        categories: DefaultDict[str, int] = defaultdict(int)

        for book in self.books.list_all():
            categories[book.Category] += 1

        return dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))

    def loans_by_user_type(self) -> Dict[str, int]:
        users: Dict[str, str] = {user.ID: user.Type for user in self.users.list_all()}
        types: DefaultDict[str, int] = defaultdict(int)
        
        for loan in self.loans.list_all():
            user_type = users.get(loan.UserID, 'Visitante')
            types[user_type] += 1
            
        return dict(sorted(types.items(), key=lambda item: item[1], reverse=True))

    def most_loaned_books(self, limit: int = 10) -> List[Tuple[str, str, int, str]]:
        books_info = {book.ISBN: (book.Title, book.Category) for book in self.books.list_all()}
        counts: DefaultDict[str, int] = defaultdict(int)
        
        for loan in self.loans.list_all():
            counts[loan.ISBN] += 1
        
        result = []
        for isbn, count in counts.items():
            title, category = books_info.get(isbn, ('Desconhecido', 'Desconhecida'))
            result.append((title, isbn, count, category))
        
        return sorted(result, key=lambda x: x[2], reverse=True)[:limit]

    def get_summary_stats(self) -> Dict[str, int]:
        return {
            'total_books': len(self.books.list_all()),
            'total_users': len(self.users.list_all()),
            'active_loans': len([loan for loan in self.loans.list_all() if not loan.ReturnDate]),
            'completed_loans': len([loan for loan in self.loans.list_all() if loan.ReturnDate]),
            'avg_loans_per_user': self._calculate_avg_loans_per_user(),
            'most_active_user': self._get_most_active_user(),
            'most_popular_category': self._get_most_popular_category()
        }

    def _calculate_avg_loans_per_user(self) -> float:
        loans_count = len(self.loans.list_all())
        users_count = len(self.users.list_all())
        return loans_count / users_count if users_count > 0 else 0

    def _get_most_active_user(self) -> str:
        user_loans: DefaultDict[str, int] = defaultdict(int)
        for loan in self.loans.list_all():
            user_loans[loan.UserID] += 1
        
        if not user_loans:
            return "Nenhum"
            
        max_user = max(user_loans.items(), key=lambda x: x[1])
        user = self.users.get_user_by_id(max_user[0])
        return f"{user.Name} ({max_user[1]} empréstimos)" if user else "Desconhecido"

    def _get_most_popular_category(self) -> str:
        category_loans: DefaultDict[str, int] = defaultdict(int)
        books_info = {book.ISBN: book.Category for book in self.books.list_all()}
        
        for loan in self.loans.list_all():
            category = books_info.get(loan.ISBN, 'Desconhecida')
            category_loans[category] += 1
        
        if not category_loans:
            return "Nenhuma"
            
        return max(category_loans.items(), key=lambda x: x[1])[0]

    def get_recent_activity(self, days: int = 30) -> List[Tuple[str, str, str, int]]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_activity: DefaultDict[Tuple[str, str], int] = defaultdict(int)
        
        for loan in self.loans.list_all():
            loan_date = loan.LoanDate if isinstance(loan.LoanDate, datetime) else datetime.strptime(loan.LoanDate, "%Y-%m-%d %H:%M:%S")
            
            if start_date.date() <= loan_date.date() <= end_date.date():
                date_str = loan_date.strftime("%d/%m/%Y")
                daily_activity[(date_str, "Empréstimo")] += 1
            
            if loan.ReturnDate:
                return_date = loan.ReturnDate if isinstance(loan.ReturnDate, datetime) else datetime.strptime(loan.ReturnDate, "%Y-%m-%d %H:%M:%S")
                
                if start_date.date() <= return_date.date() <= end_date.date():
                    date_str = return_date.strftime("%d/%m/%Y")
                    daily_activity[(date_str, "Devolução")] += 1
        
        result = []
        for (date, activity_type), count in daily_activity.items():
            description = "Livros emprestados" if activity_type == "Empréstimo" else "Livros devolvidos"
            result.append((date, activity_type, description, count))
        
        return sorted(result, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)

    def get_loans_timeline(self, days: int = 30) -> Dict[str, Dict[str, int]]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        timeline: DefaultDict[str, Dict[str, int]] = defaultdict(lambda: {"Empréstimos": 0, "Devoluções": 0})
        
        for loan in self.loans.list_all():
            loan_date = loan.LoanDate if isinstance(loan.LoanDate, datetime) else datetime.strptime(loan.LoanDate, "%Y-%m-%d %H:%M:%S")
            
            if start_date.date() <= loan_date.date() <= end_date.date():
                date_str = loan_date.strftime("%d/%m/%Y")
                timeline[date_str]["Empréstimos"] += 1
            
            if loan.ReturnDate:
                return_date = loan.ReturnDate if isinstance(loan.ReturnDate, datetime) else datetime.strptime(loan.ReturnDate, "%Y-%m-%d %H:%M:%S")
                
                if start_date.date() <= return_date.date() <= end_date.date():
                    date_str = return_date.strftime("%d/%m/%Y")
                    timeline[date_str]["Devoluções"] += 1
        
        return dict(sorted(timeline.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")), reverse=True)

    def get_user_loan_stats(self, user_id: str) -> Dict[str, Any]:
        user = self.users.get_user_by_id(user_id)
        if not user:
            return {}
            
        user_loans = [loan for loan in self.loans.list_all() if loan.UserID == user_id]
        active_loans = [loan for loan in user_loans if not loan.ReturnDate]
        favorite_category = self._get_user_favorite_category(user_id)
        
        return {
            'total_loans': len(user_loans),
            'active_loans': len(active_loans),
            'favorite_category': favorite_category,
            'avg_loan_duration': self._calculate_avg_loan_duration(user_loans),
            'last_loan_date': max(loan.LoanDate for loan in user_loans).strftime("%d/%m/%Y") if user_loans else "Nunca"
        }

    def _get_user_favorite_category(self, user_id: str) -> str:
        category_counts: DefaultDict[str, int] = defaultdict(int)
        books_info = {book.ISBN: book.Category for book in self.books.list_all()}
        
        for loan in self.loans.list_all():
            if loan.UserID == user_id:
                category = books_info.get(loan.ISBN, 'Desconhecida')
                category_counts[category] += 1
        
        return max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "Nenhuma"

    def _calculate_avg_loan_duration(self, loans: List[Loan]) -> float:
        completed_loans = [loan for loan in loans if loan.ReturnDate]
        if not completed_loans:
            return 0
            
        total_days = sum((loan.ReturnDate - loan.LoanDate).days for loan in completed_loans)
        return total_days / len(completed_loans)