from dataclasses import dataclass
from typing import Dict, Any, Literal, ClassVar

UserType = Literal['Estudante', 'Professor', 'Visitante']

@dataclass
class User:
    ALLOWED_TYPES: ClassVar[tuple[UserType, ...]] = ('Estudante', 'Professor', 'Visitante')
    
    Name: str
    Email: str
    ID: str
    Type: UserType

    def __post_init__(self) -> None:
        if self.Type not in self.ALLOWED_TYPES:
            raise ValueError(f"Tipo inválido, o tipo deve ser um dos tipos válidos: {self.ALLOWED_TYPES}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Name': self.Name,
            'Email': self.Email,
            'ID': self.ID,
            'Type': self.Type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            Name=data['Name'],
            Email=data['Email'],
            ID=data['ID'],
            Type=data['Type']
        )