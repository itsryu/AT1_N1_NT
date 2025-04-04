from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Book:
    Title: str
    Author: str
    Year: str 
    ISBN: str
    Category: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Title': self.Title,
            'Author': self.Author,
            'Year': self.Year,
            'ISBN': self.ISBN,
            'Category': self.Category
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        return cls(
            Title=data['Title'],
            Author=data['Author'],
            Year=data['Year'],
            ISBN=data['ISBN'],
            Category=data['Category']
        )