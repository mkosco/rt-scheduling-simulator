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

    """
    This is MLLF so we sort according to LLF 
    with the special case that we can also prioritize the previous job in special occasions 
    """
    def sort_jobs(self) -> list[Job]:
        # Survey of Real Time Scheduling Algorithms
        # laxity = deadline - current time - cpu time still needed
        for job in self.active_jobs:
            job.laxity = job.deadline - self.current_time - (job.execution_requirement - job.steps_executed)
        
        min_laxity_jobs: list[Job] = [job for job in sorted(self.active_jobs, key=lambda job: job.laxity)]
        
        # find Tmin, Job with smallest deadline of all active jobs and non minimal laxity
        t_min: Optional[Job] = None
        min_deadline = min(self.active_jobs, key=lambda j: j.deadline).deadline
        min_deadline_jobs = [job for job in self.active_jobs if job.laxity == min_deadline]

        for job in min_deadline_jobs:
            if job.laxity > min_laxity_jobs[0].laxity:
                t_min = job

        """ 
        check if rescheduling is necessary:
            
        Rescheduling point conditions
            1. last task Terminates
            2. last task uses up the time quantum or
            3. new tasks are requested (implicitly done in the sim)
        """
        
        if self.previous_job is not None and \
            self.previous_job in self.active_jobs and (
            self.previous_job.state is not JobState.FINNISHED or \
            self.previous_job.execution_requirement != 0 or \
            (t_min is not None and (t_min.deadline - self.previous_job.laxity) != 0)):
            # if this condition holds we need to pick the previous job if possible, therefore we put it in front
            min_laxity_jobs.remove(self.previous_job)
            min_laxity_jobs.insert(0, self.previous_job)
        
        self.previous_job = min_laxity_jobs[0]
                
        return min_laxity_jobs