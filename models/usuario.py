from dataclasses import dataclass
from typing import Dict, Any, Literal, ClassVar

TipoUsuario = Literal['Aluno', 'Professor', 'Visitante']

@dataclass
class Usuario:
    TIPOS_PERMITIDOS: ClassVar[tuple[TipoUsuario, ...]] = ('Aluno', 'Professor', 'Visitante')
    
    Nome: str
    Email: str
    ID: str
    Tipo: TipoUsuario

    def __post_init__(self):
        if self.Tipo not in self.TIPOS_PERMITIDOS:
            raise ValueError(f"Tipo de usuário inválido. Deve ser um dos: {self.TIPOS_PERMITIDOS}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Nome': self.Nome,
            'Email': self.Email,
            'ID': self.ID,
            'Tipo': self.Tipo
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Usuario':
        return cls(
            Nome=data['Nome'],
            Email=data['Email'],
            ID=data['ID'],
            Tipo=data['Tipo']
        )