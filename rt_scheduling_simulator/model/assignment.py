from dataclasses import dataclass
from typing import Optional

from rt_scheduling_simulator.model.task import Task

@dataclass
class Assignment:
    task: Task
    resource: object
    start: int
    end: int