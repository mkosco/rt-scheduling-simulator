from abc import ABC, abstractmethod
from pprint import pprint
from dataclasses import asdict
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.model.task import Task 

class Algorithm(ABC):
    def __init__(self, tasks: list[Task], resources, max_timepoint):
        self.tasks = tasks
        self.resources = resources
        self.max_timepoint = max_timepoint
        self.jobs = self.generate_jobs()
        self.active_jobs: list[Job] = []
        self.result = []
        self.current_time = 0
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        print(f"tasks: {self.tasks}")
        print(f"jobs: ")
        pprint(self.jobs)
        print(f"resources: {self.resources}")
        print(f"max timepoint: {self.max_timepoint} \n")

    @abstractmethod
    def pick_next_job(self) -> Job:
        pass

    def calculate(self) -> list:
        """This function performs the algorithm calculation"""
        i = 0
        while True:
            self.current_time = i
            self.update_active_jobs(i)
            
            if not self.active_jobs:
                return self.result
            
            print(f"timepoint: {i}, active jobs:")
            pprint(self.active_jobs)

            picked_job = self.pick_next_job()

            active_job_copy = list(map(asdict, self.active_jobs))
            
            self.result.append({'timepoint' : i, 'active_jobs' : active_job_copy})
            print(f"picked job: {picked_job}")

            picked_job.execution_requirement -= 1
            i += 1

    def generate_jobs(self) -> list[Job]:
        "This function is used to generate the joblist for the considered timeframe from the task list"
        jobs = []

        for task in self.tasks:
            print(f"\ncreating jobs for task: {task}")

            # TODO check behaviour if division is not round
            num_jobs = int(self.max_timepoint / task.period)
            print(f"number of jobs for task: {num_jobs}")
            
            for i in range(num_jobs):
                jobs.append(Job(name=f"{task.name.strip()}_j{i}",
                                arrival_time=(task.start + i * task.period),
                                execution_requirement=task.wcet,
                                deadline=(task.start + i * task.period + task.relative_deadline),
                                state=JobState.INACTIVE,
                                laxity=None))

        print(f"\njobs for taskset:\n")
        pprint(jobs)
        return jobs
    
    def update_active_jobs(self, current_time) -> None:
        """ 
        This function updates the list of currently active jobs, this list is used in algorithm calculation.\n
        A job is active when:
            1: arrival time <= current time
            2: current time <= deadline
            3: the execution requirement was not fulfilled yet
        """
        
        for job in self.jobs:
            job.state = JobState.WAITING
            job_is_active = job.arrival_time <= current_time and current_time <= job.deadline and job.execution_requirement > 0

            if job_is_active and job not in self.active_jobs:
                job.state = JobState.WAITING
                self.active_jobs.append(job)
            elif not job_is_active and job in self.active_jobs:
                if job.execution_requirement > 0:
                    job.state = JobState.MISSED
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n unfinished job: {job}")
                job.state = JobState.FINNISHED
                self.active_jobs.remove(job) 
