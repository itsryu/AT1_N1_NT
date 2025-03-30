from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Loan:
    ISBN: str
    UserID: str
    LoanDate: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ReturnDate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ISBN': self.ISBN,
            'UserID': self.UserID,
            'LoanDate': self.LoanDate,
            'ReturnDate': self.ReturnDate or ''
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Loan':
        return cls(
            ISBN=data['ISBN'],
            UserID=data['UserID'],
            LoanDate=data.get('LoanDate', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ReturnDate=data.get('ReturnDate') or None
        )