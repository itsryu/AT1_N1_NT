from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Livro:
    Título: str
    Autor: str
    Ano: str 
    ISBN: str
    Categoria: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Título': self.Título,
            'Autor': self.Autor,
            'Ano': self.Ano,
            'ISBN': self.ISBN,
            'Categoria': self.Categoria
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Livro':
        return cls(
            Título=data['Título'],
            Autor=data['Autor'],
            Ano=data['Ano'],
            ISBN=data['ISBN'],
            Categoria=data['Categoria']
        )