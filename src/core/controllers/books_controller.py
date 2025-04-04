from typing import List, Dict
from core.models.book import Book
from shared.file_manager import FileManager
from core.controllers.base_controller import BaseController

class BooksController(BaseController[Book]):
    def __init__(self) -> None:
        super().__init__(FileManager(
            filename='data/books.csv',
            headers=['Title', 'Author', 'Year', 'ISBN', 'Category'],
            model_class=Book
        ))

    def search_term(self, term: str) -> List[Book]:
        term_lower = term.lower()
        
        return [
            book for book in self.list_all()
            if any(term_lower in getattr(book, attr).lower() for attr in ['Title', 'Author', 'Category', 'Year', 'ISBN'])
        ]

    def register_book(self, book_data: Dict[str, str]) -> None:
        required_fields = {"Title", "Author", "Year", "ISBN", "Category"}
        missing_fields = [field for field in required_fields if not book_data.get(field)]

        if missing_fields:
            raise ValueError("Todos os campos são obrigatórios!")
        elif self.isbn_exists(book_data["ISBN"]):
            raise ValueError("ISBN já cadastrado!")

        self.add(Book(**book_data))

    def delete_book(self, isbn: str | int) -> None:
        isbn = str(isbn)
        book_to_remove = next((book for book in self.list_all() if book.ISBN == isbn), None)

        if not book_to_remove:
            raise ValueError("Livro não encontrado!")
        self.remove(book_to_remove)

    def isbn_exists(self, isbn: str) -> bool:
        return any(book.ISBN == isbn for book in self.list_all())
