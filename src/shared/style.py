from typing import NamedTuple, Tuple
from dataclasses import dataclass
import logging
import tkinter.font as tkfont
import tkinter as tk

class Color(NamedTuple):
    normal: str
    hover: str
    active: str

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "CRITICAL": "\033[95m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        return f"{color}{super().format(record)}{self.RESET}"

@dataclass
class ColorPalette:
    PRIMARY: str = "#3498db"
    SECONDARY: str = "#2ecc71"
    SUCCESS: str = "#27ae60"
    INFO: str = "#2980b9"
    WARNING: str = "#f39c12"
    DANGER: str = "#e74c3c"
    PURPLE: str = "#9b59b6"
    
    LIGHT: str = "#ecf0f1"
    DARK: str = "#2c3e50"
    GRAY: str = "#95a5a6"
    
    TEXT_PRIMARY: str = "#2c3e50"
    TEXT_SECONDARY: str = "#7f8c8d"
    BUTTON_TEXT: str = "#ffffff"
    
    BACKGROUND: str = "#f5f7fa"
    SURFACE: str = "#ffffff"
    
    @staticmethod
    def get_hover_color(base_color: str) -> str:
        color_map = {
            "#3498db": "#2980b9",  # PRIMARY
            "#2ecc71": "#27ae60",  # SECONDARY
            "#27ae60": "#219653",  # SUCCESS
            "#2980b9": "#1f618d",  # INFO
            "#f39c12": "#e67e22",  # WARNING
            "#e74c3c": "#c0392b",  # DANGER
            "#9b59b6": "#8e44ad",  # PURPLE
        }
        return color_map.get(base_color, ColorPalette.darken_color(base_color, 15))
    
    @staticmethod
    def get_active_color(base_color: str) -> str:
        return ColorPalette.darken_color(base_color, 25)
    
    @staticmethod
    def darken_color(hex_color: str, percent: int) -> str:
        if not hex_color.startswith('#'):
            return hex_color
            
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        darkened = []
        for component in rgb:
            darkened.append(max(0, min(255, int(component * (100 - percent) / 100))))
        
        return "#{:02x}{:02x}{:02x}".format(*darkened)
    
class FontConfig(NamedTuple):
    family: str = "Segoe UI"
    size: int = 12
    weight: str = "normal"
    slant: str = "roman"
    underline: bool = False

class Fonts:
    @staticmethod
    def _create_font(config: FontConfig) -> Tuple[str, int, str]:
        return (config.family, config.size, config.weight)
    
    TITLE: Tuple[str, int, str] = ("Arial", 24, "bold")
    SUBTITLE: Tuple[str, int, str] = ("Arial", 14, "italic")
    BUTTON: Tuple[str, int, str] = ("Segoe UI", 12, "bold")
    BODY: Tuple[str, int, str] = ("Segoe UI", 11, "normal")
    FOOTER: Tuple[str, int, str] = ("Segoe UI", 9, "italic")
    
    BODY_BOLD: Tuple[str, int, str] = ("Segoe UI", 11, "bold")
    BODY_ITALIC: Tuple[str, int, str] = ("Segoe UI", 11, "italic")
    
    SMALL: Tuple[str, int, str] = ("Segoe UI", 9, "normal")
    SMALL_BOLD: Tuple[str, int, str] = ("Segoe UI", 9, "bold")
    SMALL_ITALIC: Tuple[str, int, str] = ("Segoe UI", 9, "italic")
    
    LARGE: Tuple[str, int, str] = ("Segoe UI", 14, "normal")
    LARGE_BOLD: Tuple[str, int, str] = ("Segoe UI", 14, "bold")
    
    MONOSPACE: Tuple[str, int, str] = ("Consolas", 11, "normal")
    MONOSPACE_BOLD: Tuple[str, int, str] = ("Consolas", 11, "bold")

    @staticmethod
    def load_custom_fonts(root: tk.Tk) -> None:
        try:
            font_families = list(tkfont.families())
            
            if "Roboto" in font_families:
                Fonts.TITLE = ("Roboto", 24, "bold")
                Fonts.SUBTITLE = ("Roboto", 14, "italic")
                Fonts.BUTTON = ("Roboto", 12, "bold")
                Fonts.BODY = ("Roboto", 11, "normal")
                Fonts.FOOTER = ("Roboto", 9, "italic")
                
                Fonts.BODY_BOLD = ("Roboto", 11, "bold")
                Fonts.BODY_ITALIC = ("Roboto", 11, "italic")
                Fonts.SMALL = ("Roboto", 9, "normal")
                Fonts.SMALL_BOLD = ("Roboto", 9, "bold")
                Fonts.SMALL_ITALIC = ("Roboto", 9, "italic")
                Fonts.LARGE = ("Roboto", 14, "normal")
                Fonts.LARGE_BOLD = ("Roboto", 14, "bold")
                
            if "Fira Code" in font_families:
                Fonts.MONOSPACE = ("Fira Code", 11, "normal")
                Fonts.MONOSPACE_BOLD = ("Fira Code", 11, "bold")
                
        except Exception as e:
            print(f"Erro ao carregar fontes personalizadas: {e}")