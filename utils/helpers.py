from datetime import datetime
from typing import Any, Callable, TypeVar, cast
from utils.logger import Logger
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