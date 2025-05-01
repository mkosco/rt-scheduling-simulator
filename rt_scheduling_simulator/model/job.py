from dataclasses import dataclass
from enum import Enum

class JobState(str, Enum):
    INACTIVE = "inactive"
    WAITING = "waiting"
    EXECUTING = "executing"
    FINNISHED = "finnished"
    MISSED = "missed"

@dataclass
class Job:
    name: str
    arrival_time: int
    execution_requirement: int
    deadline: int
    state: JobState