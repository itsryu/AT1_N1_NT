from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class Loan:
    ISBN: str
    UserID: str
    LoanDate: datetime = field(default_factory=datetime.now)
    ReturnDate: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ISBN': self.ISBN,
            'UserID': self.UserID,
            'LoanDate': self.LoanDate.strftime("%Y-%m-%d %H:%M:%S.%f") if self.LoanDate else '',
            'ReturnDate': self.ReturnDate.strftime("%Y-%m-%d %H:%M:%S.%f") if self.ReturnDate else ''
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Loan':
        loan_date = datetime.strptime(data['LoanDate'], "%Y-%m-%d %H:%M:%S.%f") if data.get('LoanDate') else datetime.now()
        return_date = datetime.strptime(data['ReturnDate'], "%Y-%m-%d %H:%M:%S.%f") if data.get('ReturnDate') else None
        
        return cls(
            ISBN=data['ISBN'],
            UserID=data['UserID'],
            LoanDate=loan_date,
            ReturnDate=return_date
        )