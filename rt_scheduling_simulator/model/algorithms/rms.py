from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job
from rt_scheduling_simulator.logging import debug_print

class RMS(Algorithm):
    def summarize(self):
        debug_print(f"\nRMS")
        super().summarize()
        pass

    """ 
    This is RMS so we sort according to the smallest priority
    The shorter the period of a task the higher the priority
    """
    def sort_jobs(self) -> list[Job]:
        return [job for job in sorted(self.active_jobs, key=lambda job: job.rms_priority)]