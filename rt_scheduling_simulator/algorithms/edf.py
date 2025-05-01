from rt_scheduling_simulator.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job 

class EDF(Algorithm):
    def calculate(self):
        print("\n performing EDF: \n")
        for i in range(self.max_timepoint):
            self.update_active_jobs(i)

            picked_job = self.pick_next_job()

            print(f"timepoint: {i}, active jobs: {self.active_jobs}, picked job: {picked_job}")
    
    def summarize(self):
        print(f"\nEDF")
        super().summarize()
        pass

    """ This is EDF so we pick the job with the smallest (earliest) deadline """
    def pick_next_job(self):
        next_job: Job = self.active_jobs.pop() # initialize arbitrarily

        for job in self.active_jobs:
            if job.deadline < next_job.deadline:
                next_job = job

        return next_job
