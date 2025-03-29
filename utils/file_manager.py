import csv
import os
from typing import List, Dict, Any, TypeVar, Generic, Type
from pathlib import Path
from abc import ABC, abstractmethod

T = TypeVar('T')

class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> T:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class FileManager(Generic[T]):
    def __init__(self, filename: str, headers: List[str], model_class: Type[BaseModel]):
        self.filename = Path(filename)
        self.headers = headers
        self.model_class = model_class
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self) -> None:
        if not self.filename.exists():
            self.filename.parent.mkdir(parents=True, exist_ok=True)
            with self.filename.open('w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def add_data(self, data: T) -> None:
        with self.filename.open('a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(data.to_dict())

    def load_data(self) -> List[T]:
        data = []
        if self.filename.exists():
            with self.filename.open('r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = [self.model_class.from_dict(row) for row in reader]
        return data

    def update_data(self, new_data: List[T]) -> None:
        with self.filename.open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(item.to_dict() for item in new_data)