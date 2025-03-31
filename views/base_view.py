import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Callable
from utils.helpers import handle_errors

class BaseView(ABC):
    BUTTON_WIDTH = 25
    BUTTON_HEIGHT = 2
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 900

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.setup_ui()

    @handle_errors
    def clear_frame(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    @abstractmethod
    def setup_ui(self) -> None:
        pass

    @handle_errors
    def create_frame(
        self, parent: Optional[tk.Widget] = None, **kwargs: Any
    ) -> tk.Frame:
        frame = tk.Frame(parent or self.root, **kwargs)
        frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        return frame
    
    @handle_errors
    def center_window(self) -> None:
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        if window_width == 1:
            window_width = self.WINDOW_WIDTH
        if window_height == 1:
            window_height = self.WINDOW_HEIGHT
        
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    @handle_errors
    def create_label(self, parent: tk.Widget, text: str, **kwargs: Any) -> tk.Label:
        kwargs.setdefault("bg", "#f0f0f0")
        return tk.Label(parent, text=text, **kwargs)

    @handle_errors
    def create_entry(self, parent: tk.Widget, **kwargs: Any) -> tk.Entry:
        kwargs.setdefault("width", 40)
        return tk.Entry(parent, **kwargs)

    @handle_errors
    def create_button(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[Callable] = None,
        **kwargs: Any
    ) -> tk.Button:
        kwargs.setdefault("width", 20)
        kwargs.setdefault("fg", "white")
        return tk.Button(parent, text=text, command=command, **kwargs)

    @handle_errors
    def create_combobox(
        self, parent: tk.Widget, values: List[str], **kwargs: Any
    ) -> ttk.Combobox:
        kwargs.setdefault("width", 37)
        return ttk.Combobox(parent, values=values, **kwargs)

    @handle_errors
    def create_treeview(
        self, parent: tk.Widget, columns: List[str], **kwargs: Any
    ) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=columns, show='headings', **kwargs)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        return tree

    @handle_errors
    def show_error(self, message: str) -> None:
        messagebox.showerror("Erro", message)

    @handle_errors
    def show_success(self, message: str) -> None:
        messagebox.showinfo("Sucesso", message)

    @handle_errors
    def show_warning(self, message: str) -> None:
        messagebox.showwarning("Aviso", message)
