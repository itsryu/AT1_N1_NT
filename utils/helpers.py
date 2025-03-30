from datetime import datetime
from typing import Any, Callable, TypeVar, cast
import functools

FuncType = TypeVar("FuncType", bound=Callable[..., Any])

def format_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except Exception:
        return date_str

def handle_errors(func: FuncType) -> FuncType:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if args and hasattr(args[0], "show_error"):
                args[0].show_error(f"'{func.__name__}': {e}")
            else:
                raise e
    return cast(FuncType, wrapper)