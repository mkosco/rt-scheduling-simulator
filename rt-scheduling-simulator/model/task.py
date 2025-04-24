from dataclasses import dataclass

@dataclass
class Task:
    name: str
    start: int
    wcet: int
    period: int
    relative_deadline: int # deadline is given relative to start