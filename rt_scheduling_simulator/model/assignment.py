from dataclasses import dataclass

from rt_scheduling_simulator.model.task import Task
from rt_scheduling_simulator.model.resource import Resource

@dataclass
class Assignment:
    task_name: str
    resource_name: str
    # the start from which execution step the resource is needed
    start: int
    """ 
    the last execution step for which the resource is needed, so inclusive
    e.g. end = 5, meaning the resource is needed up until (and including) execution step 5
    """
    end: int