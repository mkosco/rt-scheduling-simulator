from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
    resources: Optional[list]
    state: JobState
    laxity: Optional[int]
    fps_priority: Optional[int]
    rms_priority: Optional[int]