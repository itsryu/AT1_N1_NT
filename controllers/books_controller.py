from typing import List, Dict
from models.book import Book
from utils.file_manager import FileManager
from controllers.base_controller import BaseController

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
            if term_lower in book.Title.lower() or 
               term_lower in book.Author.lower() or 
               term_lower in book.Category.lower() or
               term_lower in book.Year.lower() or
               term_lower in book.ISBN.lower()
        ]
    
    def register_book(self, book_data: Dict[str, str]) -> None:
        if (not book_data.get("Title") or 
            not book_data.get("Author") or 
            not book_data.get("Year") or 
            not book_data.get("ISBN") or 
            not book_data.get("Category")):
            raise ValueError("All fields are required!")
        elif self.isbn_exists(book_data["ISBN"]):
            raise ValueError("ISBN already registered!")
        
        book = Book(**book_data)
        self.add(book)

    def isbn_exists(self, isbn: str) -> bool:
        return any(book.ISBN == isbn for book in self.list_all())