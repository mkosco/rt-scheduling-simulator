from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job
from rt_scheduling_simulator.logging import debug_print
import random

class EDF(Algorithm):
    def summarize(self):
        debug_print(f"\nEDF")
        super().summarize()
        pass

    """ This is EDF so we sort the jobs according to the deadline """
    def sort_jobs(self) -> list[Job]:
        return [job for job in sorted(self.active_jobs, key=lambda job: job.deadline)]