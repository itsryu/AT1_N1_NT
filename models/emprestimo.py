from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Emprestimo:
    ISBN: str
    UserID: str
    DataEmprestimo: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    DataDevolucao: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ISBN': self.ISBN,
            'UserID': self.UserID,
            'DataEmprestimo': self.DataEmprestimo,
            'DataDevolucao': self.DataDevolucao or ''
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Emprestimo':
        return cls(
            ISBN=data['ISBN'],
            UserID=data['UserID'],
            DataEmprestimo=data.get('DataEmprestimo', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            DataDevolucao=data.get('DataDevolucao') or None
        )