from rt_scheduling_simulator.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
import random

class LLF(Algorithm):
    laxity = {}
    
    def summarize(self):
        print(f"\nLLF")
        super().summarize()
        pass

    """ This is LLF so we pick the job with the smallest laxity """
    def pick_next_job(self):
        self.update_laxity()
        min_laxity_job: list[Job] = min(self.active_jobs, key=lambda j: j.laxity)
                
        # TODO set jobstate correctly
        
        return min_laxity_job
    
    # Survey of Real Time Scheduling Algorithms
    # laxity = deadline - current time - cpu time still needed
    def update_laxity(self):
        for job in self.active_jobs:
            job.laxity = job.deadline - self.current_time - job.execution_requirement
