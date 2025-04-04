from dataclasses import dataclass
from cli.commands.base_command import BaseCommand
from core.controllers.users_controller import UsersController
from rich.table import Table

@dataclass
class UserCommand(BaseCommand[UsersController]):
    controller: UsersController = UsersController()

    def register(self) -> None:
        self.console.print("\n📝 [bold]Novo Cadastro[/bold]")

        user_data = {
            'Name': input("Nome: "),
            'Email': input("Email: "),
            'ID': input("ID: "),
            'Type': input("Tipo (Estudante/Professor/Visitante): ")
        }

        if not all(user_data.values()):
            self.console.print("\n[red]✖ Todos os campos devem ser preenchidos.[/red]")
            input("\nPressione Enter para continuar...")
            return
        
        try:
            self.controller.register_user(user_data)
            self.console.print("\n[green]✔ Usuário cadastrado com sucesso![/green]")
        except ValueError as e:
            self.console.print(f"\n[red]✖ Erro: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()

    def list_all(self) -> None:
        try:
            users = self.controller.list_all()

            if not users:
                self.console.print("\n[yellow]Nenhum usuário cadastrado.[/yellow]")
                return

            table = Table(title="👤 Usuários Cadastrados", show_lines=True )
            table.add_column("Nome", style="cyan")
            table.add_column("Email", style="magenta")
            table.add_column("ID")
            table.add_column("Tipo")

            for user in users:
                table.add_row(
                    user.Name,
                    user.Email,
                    user.ID,
                    user.Type
                )

            self.console.print(table)
        except Exception as e:
            self.console.print(f"\n[red]Erro ao listar usuários: {e}[/red]")
        finally:
            input("\nPressione Enter para continuar...")
            self.terminal.clear()

    def remove(self) -> None:
        self.console.print("\n🗑️ [bold]Remover Usuário[/bold]")
        user_id = input("ID do usuário a ser removido: ")

        if not user_id:
            self.console.print("\n[red]✖ ID não pode ser vazio.[/red]")
            input("\nPressione Enter para continuar...")
            return

        try:
            self.controller.delete_user(user_id)
            self.console.print("\n[green]✔ Usuário removido com sucesso![/green]")
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
            for user in results:
                self.console.print(
                    f"[bold]Nome:[/bold] {user.Name} | [bold]Email:[/bold] {user.Email} | [bold]ID:[/bold] {user.ID} | [bold]Tipo:[/bold] {user.Type}"
                )
                
        input("\nPressione Enter para continuar...")
        self.terminal.clear()