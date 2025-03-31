from typing import Tuple, Type
import tkinter as tk
from enum import Enum, auto
from dataclasses import dataclass
from views.base_view import BaseView
from utils.helpers import handle_errors
from utils.logger import Logger
from utils.style import ColorPalette, Fonts


class MenuAction(Enum):
    BOOKS = auto()
    USERS = auto()
    LOANS = auto()
    STATS = auto()
    EXIT = auto()


@dataclass
class MenuButtonConfig:
    text: str
    action: MenuAction
    symbol: str = "→"
    color: str = ColorPalette.PRIMARY


class MainMenu(BaseView):
    @handle_errors
    def setup_ui(self) -> None:
        Fonts.load_custom_fonts(self.root)
        self.setup_window()
        self.clear_frame()
        self.create_main_container()
        self.create_header()
        self.create_menu_buttons()
        self.create_footer()
        self.center_window()

    @handle_errors
    def setup_window(self) -> None:
        self.root.title("Sistema de Biblioteca Digital")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.root.configure(bg=ColorPalette.BACKGROUND)
        
    @handle_errors
    def create_main_container(self) -> None:
        self.main_frame = self.create_frame(
            bg=ColorPalette.BACKGROUND,
            padx=20,
            pady=20
        )
        self.main_frame.pack(expand=True, fill=tk.BOTH)
    
    @handle_errors
    def create_header(self) -> None:
        header_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND
        )
        header_frame.pack(pady=(20, 40))
        
        title_label = self.create_label(
            header_frame,
            text="📚 Sistema de Biblioteca Digital",
            font=Fonts.TITLE,
            fg=ColorPalette.TEXT_PRIMARY,
            bg=ColorPalette.BACKGROUND
        )
        title_label.pack(pady=(10, 0))
        
        subtitle_label = self.create_label(
            header_frame,
            text="Gerencie sua biblioteca de forma eficiente",
            font=Fonts.SUBTITLE,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.BACKGROUND
        )
        subtitle_label.pack()

    @handle_errors
    def get_menu_buttons_config(self) -> Tuple[MenuButtonConfig, ...]:
        return (
            MenuButtonConfig(
                text=" Cadastro de Livros",
                action=MenuAction.BOOKS,
                symbol="📖",
                color=ColorPalette.SUCCESS
            ),
            MenuButtonConfig(
                text=" Cadastro de Usuários",
                action=MenuAction.USERS,
                symbol="👥",
                color=ColorPalette.INFO
            ),
            MenuButtonConfig(
                text=" Sistema de Empréstimos",
                action=MenuAction.LOANS,
                symbol="🔄",
                color=ColorPalette.WARNING
            ),
            MenuButtonConfig(
                text=" Estatísticas e Relatórios",
                action=MenuAction.STATS,
                symbol="📊",
                color=ColorPalette.PURPLE
            ),
            MenuButtonConfig(
                text=" Sair do Sistema",
                action=MenuAction.EXIT,
                symbol="🚪",
                color=ColorPalette.DANGER
            ),
        )
    
    @handle_errors
    def create_menu_buttons(self) -> None:
        buttons_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND
        )
        buttons_frame.pack(expand=True, fill=tk.BOTH)
        
        for config in self.get_menu_buttons_config():
            self.create_menu_button(buttons_frame, config)
    
    @handle_errors
    def create_menu_button(self, parent: tk.Widget, config: MenuButtonConfig) -> None:
        button_frame = self.create_frame(
            parent,
            bg=ColorPalette.BACKGROUND,
            padx=10,
            pady=8
        )
        button_frame.pack(fill=tk.X)
        
        button_text = f"{config.symbol}  {config.text}"
        
        button = tk.Button(
            button_frame,
            text=button_text,
            command=lambda: self.handle_menu_action(config.action),
            bg=config.color,
            fg=ColorPalette.BUTTON_TEXT,
            activebackground=ColorPalette.get_active_color(config.color),
            activeforeground=ColorPalette.BUTTON_TEXT,
            font=Fonts.BUTTON,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            borderwidth=0,
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            padx=10
        )
        
        button.bind("<Enter>", lambda e: button.config(
            bg=ColorPalette.get_hover_color(config.color))
        )
        button.bind("<Leave>", lambda e: button.config(
            bg=config.color)
        )
        
        button.pack(fill=tk.X, ipady=5)
        
    @handle_errors
    def handle_menu_action(self, action: MenuAction) -> None:
        action_handlers = {
            MenuAction.BOOKS: self.open_books_view,
            MenuAction.USERS: self.open_users_view,
            MenuAction.LOANS: self.open_loans_view,
            MenuAction.STATS: self.open_statistics_view,
            MenuAction.EXIT: self.exit_app,
        }
        
        handler = action_handlers.get(action)
        if handler:
            handler()
    
    @handle_errors
    def create_footer(self) -> None:
        footer_frame = self.create_frame(
            self.main_frame,
            bg=ColorPalette.BACKGROUND,
            pady=20
        )
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        version_label = self.create_label(
            footer_frame,
            text="Versão 1.0.0 © 2025 Biblioteca Digital",
            font=Fonts.FOOTER,
            fg=ColorPalette.TEXT_SECONDARY,
            bg=ColorPalette.BACKGROUND
        )
        version_label.pack()
        
    @handle_errors
    def open_books_view(self) -> None:
        from views.books_view import BooksView
        self.navigate_to_view(BooksView)
        
    @handle_errors
    def open_users_view(self) -> None:
        from views.users_view import UsersView
        self.navigate_to_view(UsersView)
        
    @handle_errors
    def open_loans_view(self) -> None:
        from views.loans_view import LoansView
        self.navigate_to_view(LoansView)
        
    @handle_errors
    def open_statistics_view(self) -> None:
        from views.statistics_view import StatisticsView
        self.navigate_to_view(StatisticsView)
        
    @handle_errors
    def navigate_to_view(self, view_class: Type[BaseView]) -> None:
        self.clear_frame()
        view_class(self.root)
        
    @handle_errors
    def exit_app(self) -> None:
        Logger.info("Encerrando aplicação...")
        self.root.quit()
        
    @handle_errors
    def start_app(self) -> None:
        Logger.info("Iniciando aplicação...")
        self.root.mainloop()