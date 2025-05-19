from rt_scheduling_simulator.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import JobState
from rt_scheduling_simulator.logging import debug_print
class RMS(Algorithm):
    def summarize(self):
        debug_print(f"\nRMS")
        super().summarize()
        pass

    """ 
        This is RMS so we pick the job with the smallest priority
        The shorter the period of a task the higher the priority
    """
    def pick_next_job(self):
        next_job = min(self.active_jobs, key=lambda j: j.rms_priority)
        
        # TODO can two task have the same priority?
        
        next_job.state = JobState.EXECUTING
        return next_job
