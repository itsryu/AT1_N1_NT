from dataclasses import dataclass
from core.controllers.books_controller import BooksController
from cli.commands.base_command import BaseCommand
from rich.table import Table

@dataclass
class BookCommands(BaseCommand[BooksController]):
    controller: BooksController = BooksController()

    def register(self) -> None:
        self.console.print("\n📝 [bold]Novo Cadastro[/bold]")
        book_data = {
            'Title': input("Título: "),
            'Author': input("Autor: "),
            'Year': input("Ano: "),
            'ISBN': input("ISBN: "),
            'Category': input("Categoria: ")
        }
        
        if not all(book_data.values()):
            self.console.print("\n[red]✖ Todos os campos devem ser preenchidos.[/red]")
            input("\nPressione Enter para continuar...")
            return
        
        try:
            self.controller.register_book(book_data)
            self.console.print("\n[green]✔ Livro cadastrado com sucesso![/green]")
        except ValueError as e:
            self.console.print(f"\n[red]✖ Erro: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()
    
    def list_all(self):
        try:
            books = self.controller.list_all()
            
            if not books:
                self.console.print("\n[yellow]Nenhum livro cadastrado.[/yellow]")
                return

            table = Table(title="📚 Acervo Completo", show_lines=True)
            table.add_column("Título", style="cyan")
            table.add_column("Autor", style="magenta")
            table.add_column("Ano")
            table.add_column("ISBN")
            table.add_column("Categoria")

            for book in books:
                table.add_row(
                    book.Title,
                    book.Author,
                    book.Year,
                    book.ISBN,
                    book.Category
                )

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar livros: {e}[/red]")
        finally:
            input("\nPressione Enter para voltar...")
            self.terminal.clear()

    def remove(self) -> None:
        self.console.print("\n🗑️ [bold]Remover Livro[/bold]")
        isbn = input("ISBN do livro a ser removido: ")

        if not isbn:
            self.console.print("\n[red]✖ ISBN não pode ser vazio.[/red]")
            input("\nPressione Enter para continuar...")
            return

        try:
            self.controller.delete_book(isbn)
            self.console.print("\n[green]✔ Livro removido com sucesso![/green]")
        except ValueError as e:
            self.console.print(f"\n[red]✖ Erro: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()
    
    def search(self) -> None:
        term = input("\n🔍 Termo de busca: ")
        results = self.controller.search_term(term)
        
        if not results:
            self.console.print("\n[yellow]Nenhum livro encontrado.[/yellow]")
        else:
            for book in results:
                self.console.print(
                    f"\n[b]{book.Title}[/b] por {book.Author} "
                    f"({book.Year}) - [i]{book.Category}[/i]"
                )
                
        input("\nPressione Enter para voltar...")
        self.terminal.clear()