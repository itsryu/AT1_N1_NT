from dataclasses import dataclass
from core.controllers.loans_controller import LoansController
from core.controllers.books_controller import BooksController
from core.controllers.users_controller import UsersController
from shared.helpers import format_date
from cli.commands.base_command import BaseCommand
from rich.table import Table

@dataclass
class LoanCommand(BaseCommand[LoansController]):
    controller: LoansController = LoansController()
    books_controller: BooksController = BooksController()
    users_controller: UsersController = UsersController()

    def register(self) -> None:
        self.console.print("\n📝 [bold]Novo Empréstimo[/bold]")
        isbn = input("ISBN do Livro: ")
        user_id = input("ID do Usuário: ")

        if not isbn or not user_id:
            self.console.print("\n[red]✖ Todos os campos devem ser preenchidos.[/red]")
            input("\nPressione Enter para continuar...")
            return

        try:
            self.controller.register_loan(isbn, user_id)
            self.console.print("\n[green]✔ Empréstimo registrado com sucesso![/green]")
        except ValueError as e:
            self.console.print(f"\n[red]✖ Erro: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()

    def list_active(self) -> None:
        try:
            loans = self.controller.list_active()
            books = {b.ISBN: b.Title for b in self.books_controller.list_all()}
            users = {u.ID: u.Name for u in self.users_controller.list_all()}

            if not loans:
                self.console.print("\n[yellow]Nenhum empréstimo ativo.[/yellow]")
                return

            table = Table(title="📚 Empréstimos Ativos", show_lines=True)
            table.add_column("ISBN", style="cyan")
            table.add_column("Título", style="magenta")
            table.add_column("ID do Usuário", style="magenta")
            table.add_column("Nome do Usuário", style="magenta")
            table.add_column("Data do Empréstimo")
            table.add_column("Status")

            for loan in loans:
                row_style = "red" if self.controller.is_loan_late(loan.ISBN, loan.UserID) else ""

                table.add_row(
                    loan.ISBN,
                    books.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    "Atrasado" if self.controller.is_loan_late(loan.ISBN, loan.UserID) else loan.ReturnDate.strftime("%d/%m/%Y") if loan.ReturnDate else "Ativo",
                    style=row_style
                )

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar empréstimos: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()

    def list_returned(self) -> None:
        try:
            loans = self.controller.list_returned()
            books = {b.ISBN: b.Title for b in self.books_controller.list_all()}
            users = {u.ID: u.Name for u in self.users_controller.list_all()}

            if not loans:
                self.console.print("\n[yellow]Nenhum empréstimo devolvido.[/yellow]")
                return

            table = Table(title="📚 Empréstimos Devolvidos", show_lines=True)
            table.add_column("ISBN", style="cyan")
            table.add_column("Título", style="magenta")
            table.add_column("ID do Usuário", style="magenta")
            table.add_column("Nome do Usuário", style="magenta")
            table.add_column("Data do Empréstimo")
            table.add_column("Data de Devolução")

            for loan in loans:
                table.add_row(
                    loan.ISBN,
                    books.get(loan.ISBN, "Desconhecido"),
                    loan.UserID,
                    users.get(loan.UserID, "Desconhecido"),
                    format_date(loan.LoanDate),
                    format_date(loan.ReturnDate) if loan.ReturnDate else "Não devolvido"
                )

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar empréstimos: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()

    def register_return(self) -> None:
        self.console.print("\n📝 [bold]Registrar Devolução[/bold]")
        isbn = input("ISBN do Livro: ")
        user_id = input("ID do Usuário: ")

        if not isbn or not user_id:
            self.console.print("\n[red]✖ Todos os campos devem ser preenchidos.[/red]")
            input("\nPressione Enter para continuar...")
            return

        try:
            if self.controller.register_return(isbn, user_id):
                self.console.print("\n[green]✔ Devolução registrada com sucesso![/green]")
            else:
                self.console.print("\n[yellow]Nenhum empréstimo encontrado para este livro e usuário.[/yellow]")
        except ValueError as e:
            self.console.print(f"\n[red]✖ Erro: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()