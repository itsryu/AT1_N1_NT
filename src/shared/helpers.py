from datetime import datetime
from typing import Any, Callable, TypeVar, cast, List
from shared.logger import Logger
import functools

FuncType = TypeVar("FuncType", bound=Callable[..., Any])

def format_date(date: datetime) -> str:
    try:
        return date.strftime("%d/%m/%Y às %H:%M")
    except Exception:
        return str(date)

def handle_errors(func: FuncType) -> FuncType:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if args and hasattr(args[0], "show_error"):
                args[0].show_error(f"'{func.__name__}': {e}")
                Logger.error(f"Error in '{func.__name__}': {e}")
            else:
                raise e
    return cast(FuncType, wrapper)


def format_header(title: str, subtitle: str = "") -> str:
    header = f"\n{'='*50}\n{title.center(50)}\n"
    if subtitle:
        header += f"{subtitle.center(50)}\n"
    header += f"{'='*50}"
    return header

def format_table(headers: List[str], rows: List[List[str]]) -> str:
    col_widths = [
        max(len(str(row[i])) for row in rows + [headers] for i in range(len(headers)))
    ]
    
    separator = "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+"
    table = [separator]
    
    header_row = "| " + " | ".join(
        f"{header:<{col_widths[i]}}" for i, header in enumerate(headers)
    ) + " |"
    table.extend([header_row, separator])
    
    for row in rows:
        data_row = "| " + " | ".join(
            f"{cell:<{col_widths[i]}}" for i, cell in enumerate(row)
        ) + " |"
        table.append(data_row)
    
    table.append(separator)
    return "\n".join(table)

def format_footer(text: str) -> str:
    return f"\n{'-'*50}\n{text.center(50)}\n{'-'*50}"

def validate_menu_choice(choice: str, valid_options: list[str]) -> bool:
    return choice in valid_options

def validate_isbn(isbn: str) -> bool:
    clean_isbn = isbn.replace("-", "")
    return clean_isbn.isdigit() and len(clean_isbn) in (10, 13)

def validate_year(year: str) -> bool:
    return year.isdigit() and len(year) == 4
