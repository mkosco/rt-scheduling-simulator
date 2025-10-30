from dataclasses import dataclass
from typing import Optional

@dataclass
class Resource:
    name: str
    priority_ceiling: Optional[int]