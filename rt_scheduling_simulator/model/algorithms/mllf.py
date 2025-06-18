from typing import Optional
from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.logging import debug_print

class MLLF(Algorithm):
    def __init__(self, tasks, resources, assignments, max_timepoint):
        super().__init__(tasks, resources, assignments, max_timepoint)
        self.previous_job: Optional[Job] = None
        
    def summarize(self):
        debug_print(f"\nMLLF")
        super().summarize()
        pass

    def pick_next_job(self):
        self.update_laxity()
        
        min_laxity_job: int = min(self.active_jobs, key=lambda j: j.laxity)
        min_laxity_jobs: list[Job] = [job for job in self.active_jobs if job.laxity == min_laxity_job.laxity]
        
        # find Tmin, Job with smallest deadline of all active jobs and non minimal laxity
        t_min: Optional[Job] = None
        min_deadline = min(self.active_jobs, key=lambda j: j.deadline).deadline
        min_deadline_jobs = [job for job in self.active_jobs if job.laxity == min_deadline]

        for job in min_deadline_jobs:
            if job.laxity > min_laxity_job.laxity:
                t_min = job

        """ check if rescheduling is necessary:
            
            Rescheduling point conditions
                1. last task Terminates
                2. last task uses up the time quantum or
                3. new tasks are requested
        """
        
        """ 
            TODO also reschedule when new tasks are available 
            although i'm not so sure i need to check this specifically anymore,
            as if a new task is released it is already checked in the conditions
        """
        if self.previous_job is not None and (
            self.previous_job.state is not JobState.FINNISHED or \
            self.previous_job.execution_requirement != 0 or \
            (t_min is not None and (t_min.deadline - self.previous_job.laxity) != 0)):
            return self.previous_job
        
        next_job = min_laxity_job
        self.previous_job = next_job
    
        next_job.state = JobState.EXECUTING
            
        return next_job
    
    # Survey of Real Time Scheduling Algorithms
    # laxity = deadline - current time - cpu time still needed
    def update_laxity(self):
        for job in self.active_jobs:
            job.laxity = job.deadline - self.current_time - job.execution_requirement
