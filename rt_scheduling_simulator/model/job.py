from dataclasses import dataclass
from enum import Enum
from typing import Optional

from rt_scheduling_simulator.model.resource import Resource

class JobState(str, Enum):
    # job not yet ready to be executed
    INACTIVE = "inactive"
    # job is ready to be executed but not executing yet
    WAITING = "waiting"
    # the job is waiting for resources
    BLOCKED = "blocked"
    # job is currently beeing executed
    EXECUTING = "executing"
    # job has it's steps executed matching the execution requirenment
    FINNISHED = "finnished"
    # the job is no longer active but has not had it's execution requirement fulfilled
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
    # this priority is either set by pip or pcp
    protocol_priority: Optional[int]