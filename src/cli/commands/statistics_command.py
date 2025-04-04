from dataclasses import dataclass
from core.controllers.statistics_controller import StatisticsController
from cli.commands.base_command import BaseCommand
from rich.table import Table
from shared.components import PDFReport

@dataclass
class StatisticsCommand(BaseCommand[StatisticsController]):
    controller: StatisticsController = StatisticsController()

    def show_books_by_category(self) -> None:
        try:
            statistics = self.controller.books_by_category()

            if not statistics:
                self.console.print("\n[yellow]Nenhum livro encontrado.[/yellow]")
                return

            total_books = sum(statistics.values())

            table = Table(title="📚 Livros por Categoria", show_lines=True)
            table.add_column("Categoria", style="cyan")
            table.add_column("Quantidade", style="magenta")
            table.add_column("Percentual", style="green")

            for category, count in statistics.items():
                percentage = (count / total_books) * 100
                table.add_row(category, str(count), f"{percentage:.2f}%")

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar livros por categoria: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")

    def show_loans_by_user_type(self) -> None:
        try:
            statistics = self.controller.loans_by_user_type()

            if not statistics:
                self.console.print("\n[yellow]Nenhum usuário encontrado.[/yellow]")
                return

            total_users = sum(statistics.values())

            table = Table(title="👤 Usuários por Tipo", show_lines=True)
            table.add_column("Tipo", style="cyan")
            table.add_column("Quantidade", style="magenta")
            table.add_column("Percentual", style="green")

            for user_type, count in statistics.items():
                percentage = (count / total_users) * 100
                table.add_row(user_type, str(count), f"{percentage:.2f}%")

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar usuários por tipo: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")

    def show_most_loaned_books(self) -> None:
        try:
            try:
                quantity = int(input("\nDigite a quantidade de livros a exibir: ") or 10)
            except ValueError:
                self.console.print("\n[yellow]Entrada inválida. Exibindo os 10 mais emprestados por padrão.[/yellow]")
                quantity = 10

            statistics = self.controller.most_loaned_books()

            if not statistics:
                self.console.print("\n[yellow]Nenhum livro encontrado.[/yellow]")
                return

            table = Table(title=f"📚 Top {quantity} Livros Mais Emprestados", show_lines=True)
            table.add_column("Título", style="cyan")
            table.add_column("ISBN", style="magenta")
            table.add_column("Quantidade de Empréstimos", style="green")
            table.add_column("Categoria", style="blue")

            for title, isbn, count, category in statistics[:quantity]:
                table.add_row(title, isbn, str(count), category)

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar livros mais emprestados: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")

    def generate_pdf_report(self) -> None:
        try:
            pdf = PDFReport(self.controller)
            path = pdf.generate()
            self.console.print(f"\n[green]✔ Relatório PDF gerado com sucesso em {path} ![/green]")
        except Exception as e:
            self.console.print(f"\n[red]Erro ao gerar relatório PDF: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")