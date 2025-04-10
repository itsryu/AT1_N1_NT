from rich.console import Console
from rich.panel import Panel
from rich import box
from shared.terminal import TerminalUtils
from shared.__version__ import __version__
from datetime import datetime
from typing import Dict, Tuple, Callable, Optional

class BaseMenu:
    def __init__(self) -> None:
        self.console: Console = Console()
        self.terminal: TerminalUtils = TerminalUtils()
        self.title: str = "Menu Principal"
        self.footer: str = f"Versão {__version__} © {datetime.now().year} Biblioteca Digital"
        self.options: Dict[str, Tuple[str, Optional[Callable[[], None]]]] = {}
    
    def display(self) -> None:
        while True:
            self.terminal.clear()
            self._show_menu()
            if (choice := self._get_choice()) in self.options:
                if (action := self.options[choice][1]):
                    action()

    def _show_menu(self) -> None:
        menu_items: list[str] = [
            f"[bold]{key}[/bold] - {label}"
            for key, (label, _) in self.options.items()
        ]
        
        self.console.print(
            Panel(
                "\n".join(menu_items),
                title=f"[bold]{self.title}[/bold]",
                border_style="blue",
                box=box.DOUBLE,
                width=60,
                padding=(1, 4)
            ),
            justify="center"
        )
        self.console.print(f"[dim]{self.footer}[/dim]", justify="center")

    def back(self) -> None:
        self.terminal.clear()
        raise StopIteration
    
    def _get_choice(self) -> str:
        while (choice := input("👉 Sua escolha: ").strip()) not in self.options:
            self.console.print("[red]Opção inválida![/red] Tente novamente.")
        return choice