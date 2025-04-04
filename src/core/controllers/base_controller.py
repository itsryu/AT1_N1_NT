from typing import List, TypeVar, Generic
from shared.file_manager import FileManager, BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseController(Generic[T]):
    def __init__(self, file_manager: FileManager[T]):
        self.file_manager = file_manager

    def list_all(self) -> List[T]:
        return self.file_manager.load_data()

    def add(self, item: T) -> None:
        self.file_manager.add_data(item)

    def remove(self, item: T) -> None:
        items = self.list_all()
        items.remove(item)
        self.file_manager.update_data(items)

    def update_all(self, items: List[T]) -> None:
        self.file_manager.update_data(items)