from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job
from rt_scheduling_simulator.logging import debug_print

class FPS(Algorithm):
    def summarize(self):
        debug_print(f"\nFPS")
        super().summarize()
        pass

    """ 
    This is FPS so we sort according to the highest priority 
    One is the highets priority, higher integers mean a lower priority
    """
    def sort_jobs(self) -> list[Job]:
        return [job for job in sorted(self.active_jobs, key=lambda job: job.fps_priority)]
