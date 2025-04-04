import csv
from typing import List, Dict, Any, TypeVar, Generic, Type
from pathlib import Path
from abc import ABC, abstractmethod
from shared.logger import Logger

T = TypeVar("T", bound="BaseModel")

class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T: ...

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]: ...


class FileManager(Generic[T]):
    def __init__(self, filename: str, headers: List[str], model_class: Type[T]) -> None:
        self.filename: Path = Path(filename)
        self.headers: List[str] = headers
        self.model_class: Type[T] = model_class
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self) -> None:
        try:
            if not self.filename.exists():
                self.filename.parent.mkdir(parents=True, exist_ok=True)
                with self.filename.open("w", newline="", encoding="utf-8-sig") as file:
                    writer = csv.DictWriter(file, fieldnames=self.headers)
                    writer.writeheader()
        except Exception as e:
            Logger.error(f"Error creating file {self.filename}: {e}")
            raise

    def add_data(self, data: T) -> None:
        try:
            with self.filename.open("a", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(data.to_dict())
        except Exception as e:
            Logger.error(f"Error adding data to {self.filename}: {e}")
            raise

    def load_data(self) -> List[T]:
        items: List[T] = []
        try:
            if self.filename.exists():
                with self.filename.open("r", encoding="utf-8-sig") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            item = self.model_class.from_dict(row)
                            items.append(item)
                        except Exception as parse_error:
                            Logger.error(f"Error parsing row {row}: {parse_error}")
            
            return items
        except Exception as e:
            Logger.error(f"Error loading data from {self.filename}: {e}")
            raise

    def update_data(self, new_data: List[T]) -> None:
        try:
            with self.filename.open("w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                for item in new_data:
                    writer.writerow(item.to_dict())
        except Exception as e:
            Logger.error(f"Error updating data in {self.filename}: {e}")
            raise
