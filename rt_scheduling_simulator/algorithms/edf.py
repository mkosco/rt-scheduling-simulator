from rt_scheduling_simulator.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job
import random

class EDF(Algorithm):
    def calculate(self):
        print("\n performing EDF: \n")
        super().calculate()

    def summarize(self):
        print(f"\nEDF")
        super().summarize()
        pass

    """ This is EDF so we pick the job with the smallest (earliest) deadline """
    def pick_next_job(self):
        next_job: Job = random.choice(self.active_jobs) # initialize arbitrarily

        for job in self.active_jobs:
            if job.deadline < next_job.deadline:
                next_job = job

        return next_job
