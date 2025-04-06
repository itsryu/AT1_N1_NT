from rich.console import Console
from rich.panel import Panel
from rich import box
from shared.terminal import TerminalUtils
from shared.__version__ import __version__
from datetime import datetime

class BaseMenu:
    def __init__(self):
        self.console = Console()
        self.terminal = TerminalUtils()
        self.title = "Menu Principal"
        self.footer = f"Versão {__version__} © {datetime.now().strftime("%Y")} Biblioteca Digital"
        self.options = {}
    
    def display(self):
        while True:
            self.terminal.clear()
            self._show_menu()
            choice = self._get_choice()

            if choice in self.options:
                _, action = self.options[choice]

                if action:
                    action()

    def _show_menu(self):
        menu_items = [
            f"[bold]{key}[/bold] - {label}"
            for key, (label, _) in self.options.items()
        ]
        
        panel = Panel(
            "\n".join(menu_items),
            title=f"[bold]{self.title}[/bold]",
            border_style="blue",
            box=box.DOUBLE,
            width=60,
            padding=(1, 4)
        )
        
        self.console.print(panel, justify="center")
        self.console.print(f"[dim]{self.footer}[/dim]", justify="center")

    def back(self):
        self.terminal.clear()
        raise StopIteration
    
    def _get_choice(self):
        while True:
            choice = input("👉 Sua escolha: ").strip()
            
            if choice in self.options:
                return choice
            
            self.console.print("[red]Opção inválida![/red] Tente novamente.")