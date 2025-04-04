import os
import platform
from typing import Optional
from rich.console import Console

class TerminalUtils:
    def __init__(self):
        self.console = Console()
        self.is_jupyter = self._check_jupyter()
    
    def _check_jupyter(self) -> bool:
        try:
            from IPython import get_ipython
            return 'IPKernelApp' in get_ipython().config
        except:
            return False
    
    def clear(self, fallback_lines: int = 100) -> None:
        methods = [
            self._try_rich_clear,
            self._try_ansi_escape,
            self._try_system_clear,
            lambda: print("\n" * fallback_lines)
        ]
        
        for method in methods:
            try:
                method()
                return
            except:
                continue
    
    def _try_rich_clear(self) -> None:
        if hasattr(self.console, 'clear'):
            self.console.clear()
    
    def _try_ansi_escape(self) -> None:
        print("\033[H\033[J", end="")
    
    def _try_system_clear(self) -> None:
        if self.is_jupyter:
            from IPython.display import display, HTML
            display(HTML('<style>.output_area { height: auto !important; }</style>'))
            print("\n" * 10)
        elif os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')