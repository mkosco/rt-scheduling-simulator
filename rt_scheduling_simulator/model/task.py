from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    name: str
    start: int
    wcet: int
    period: int
    relative_deadline: int # deadline is given relative to start
    priority: Optional[int]