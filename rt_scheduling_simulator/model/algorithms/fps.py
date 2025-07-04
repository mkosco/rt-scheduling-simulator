from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.logging import debug_print

class FPS(Algorithm):
    def summarize(self):
        debug_print(f"\nFPS")
        super().summarize()
        pass

    """ 
        This is FPS so we pick the job with the highest priority 

        One is the highets priority, higher integers mean a lower priority
    """
    def pick_next_job(self):
        next_job = min(self.active_jobs, key=lambda j: j.fps_priority)
        
        # TODO can two task have the same priority?
        
        next_job.state = JobState.EXECUTING
        return next_job
