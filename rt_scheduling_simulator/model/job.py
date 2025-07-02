from dataclasses import dataclass
from enum import Enum
from typing import Optional

from rt_scheduling_simulator.model.resource import Resource

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
    steps_executed: int
    deadline: int
    # describes the resources needed for the corresponding execution requirement
    resources_needed: Optional[list[Resource]]
    state: JobState
    laxity: Optional[int]
    fps_priority: Optional[int]
    rms_priority: Optional[int]