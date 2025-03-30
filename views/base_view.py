import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Callable

class BaseView(ABC):
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.setup_ui()

    def clear_frame(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    @abstractmethod
    def setup_ui(self) -> None:
        pass

    def create_frame(
        self, parent: Optional[tk.Widget] = None, **kwargs: Any
    ) -> tk.Frame:
        frame = tk.Frame(parent or self.root, **kwargs)
        frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        return frame

    def create_label(self, parent: tk.Widget, text: str, **kwargs: Any) -> tk.Label:
        kwargs.setdefault("bg", "#f0f0f0")
        return tk.Label(parent, text=text, **kwargs)

    def create_entry(self, parent: tk.Widget, **kwargs: Any) -> tk.Entry:
        kwargs.setdefault("width", 40)
        return tk.Entry(parent, **kwargs)

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

    def create_combobox(
        self, parent: tk.Widget, values: List[str], **kwargs: Any
    ) -> ttk.Combobox:
        kwargs.setdefault("width", 37)
        return ttk.Combobox(parent, values=values, **kwargs)

    def create_treeview(
        self, parent: tk.Widget, columns: List[str], **kwargs: Any
    ) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=columns, show='headings', **kwargs)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        return tree

    def show_error(self, message: str) -> None:
        messagebox.showerror("Erro", message)

    def show_success(self, message: str) -> None:
        messagebox.showinfo("Sucesso", message)

    def show_warning(self, message: str) -> None:
        messagebox.showwarning("Aviso", message)
