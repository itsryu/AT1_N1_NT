from dataclasses import dataclass
from typing import Dict
from core.controllers.statistics_controller import StatisticsController
from cli.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from shared.components import PDFReport

@dataclass
class StatisticsCommand(BaseCommand[StatisticsController]):
    controller: StatisticsController = StatisticsController()

    def _show_ascii_bar_chart(self, data: Dict[str, int], title: str) -> None:
        if not data:
            self.console.print("\n[yellow]Nenhum dado para exibir.[/yellow]")
            return

        max_value = max(data.values()) if max(data.values()) > 0 else 1
        max_label_length = max(len(str(k)) for k in data.keys())
        chart_lines = [f"\n[bold]{title}[/bold]", ""]

        for label, value in data.items():
            bar_length = int((value / max_value) * 50)
            bar = '█' * bar_length
            percentage = (value / sum(data.values())) * 100
            chart_lines.append(
                f"[cyan]{label.ljust(max_label_length)}[/cyan] | "
                f"[green]{bar}[/green] "
                f"[magenta]{value} ({percentage:.1f}%)[/magenta]"
            )

        self.console.print(Panel("\n".join(chart_lines), border_style="blue"))

    def show_books_by_category(self, view_type: str = 'table') -> None:
        try:
            statistics = self.controller.books_by_category()

            if not statistics:
                self.console.print("\n[yellow]Nenhum livro encontrado.[/yellow]")
                return

            if view_type == 'bar':
                self._show_ascii_bar_chart(statistics, "📊 Livros por Categoria")
            else:
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
            self.console.print(f"\n[red]Erro ao gerar estatísticas: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")

    def show_loans_by_user_type(self, view_type: str = 'table') -> None:
        try:
            statistics = self.controller.loans_by_user_type()

            if not statistics:
                self.console.print("\n[yellow]Nenhum dado de empréstimo encontrado.[/yellow]")
                return

            if view_type == 'bar':
                self._show_ascii_bar_chart(statistics, "📊 Empréstimos por Tipo de Usuário")
            else:
                total_users = sum(statistics.values())
                table = Table(title="👤 Empréstimos por Tipo de Usuário", show_lines=True)
                table.add_column("Tipo", style="cyan")
                table.add_column("Quantidade", style="magenta")
                table.add_column("Percentual", style="green")

                for user_type, count in statistics.items():
                    percentage = (count / total_users) * 100
                    table.add_row(user_type, str(count), f"{percentage:.2f}%")

                self.console.print(table)

        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar empréstimos: {e}[/red]")
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
                self.console.print("\n[yellow]Nenhum dado de empréstimo encontrado.[/yellow]")
                return

            table = Table(title=f"📚 Top {quantity} Livros Mais Emprestados", show_lines=True)
            table.add_column("Posição", style="cyan")
            table.add_column("Título", style="magenta")
            table.add_column("ISBN", style="green")
            table.add_column("Empréstimos", style="blue")
            table.add_column("Categoria", style="yellow")

            for i, (title, isbn, count, category) in enumerate(statistics[:quantity], 1):
                table.add_row(str(i), title, isbn, str(count), category)

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