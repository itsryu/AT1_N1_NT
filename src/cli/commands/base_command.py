from typing import TypeVar, Generic
from core.controllers.base_controller import BaseController
from rich.console import Console
from shared.terminal import TerminalUtils

T = TypeVar('T', bound=BaseController)

class BaseCommand(Generic[T]):
    console: Console = Console()
    terminal: TerminalUtils = TerminalUtils()

    def __init__(self, controller: BaseController[T]) -> None:
        self.controller: BaseController[T] = controller