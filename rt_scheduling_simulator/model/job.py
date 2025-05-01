from dataclasses import dataclass

@dataclass
class Job:
    name: str
    arrival_time: int
    execution_requirement: int
    deadline: int