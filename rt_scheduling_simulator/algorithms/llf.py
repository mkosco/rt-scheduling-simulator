from rt_scheduling_simulator.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.logging import debug_print

class LLF(Algorithm):
    laxity = {}
    
    def summarize(self):
        debug_print(f"\nLLF")
        super().summarize()
        pass

    """ This is LLF so we pick the job with the smallest laxity """
    def pick_next_job(self):
        self.update_laxity()
        min_laxity_job: Job = min(self.active_jobs, key=lambda j: j.laxity)
                
        min_laxity_job.state = JobState.EXECUTING
        
        return min_laxity_job
    
    # Survey of Real Time Scheduling Algorithms
    # laxity = deadline - current time - cpu time still needed
    def update_laxity(self):
        for job in self.active_jobs:
            job.laxity = job.deadline - self.current_time - job.execution_requirement
