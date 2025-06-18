from dataclasses import dataclass

from rt_scheduling_simulator.model.task import Task
from rt_scheduling_simulator.model.resource import Resource

@dataclass
class Assignment:
    task_name: str
    resource_name: str
    start: int
    end: int