from datetime import datetime
from typing import List, Dict, Any

def formatar_data(data_str: str) -> str:
    try:
        return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except:
        return data_str