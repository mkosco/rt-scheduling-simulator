from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job
from rt_scheduling_simulator.logging import debug_print

class LLF(Algorithm):
    laxity = {}
    
    def summarize(self):
        debug_print(f"\nLLF")
        super().summarize()
        pass

    """ This is LLF so we sort according to the smallest laxity """
    def sort_jobs(self) -> list[Job]:
        # Survey of Real Time Scheduling Algorithms
        # laxity = deadline - current time - cpu time still needed
        for job in self.active_jobs:
            job.laxity = job.deadline - self.current_time - job.execution_requirement
                        
        return [job for job in sorted(self.active_jobs, key=lambda job: job.laxity)]