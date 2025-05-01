from abc import ABC, abstractmethod
from pprint import pprint
from rt_scheduling_simulator.model.job import Job
from rt_scheduling_simulator.model.task import Task 

class Algorithm(ABC):
    def __init__(self, tasks: list[Task], resources, max_timepoint):
        self.tasks = tasks
        self.resources = resources
        self.max_timepoint = max_timepoint
        self.jobs = self.generate_jobs()
        self.active_jobs: list[Job] = []

    @abstractmethod
    def calculate(self) -> None:
        """This function performs the algorithm calculation"""
        for i in range(self.max_timepoint):
            self.update_active_jobs(i)

            picked_job = self.pick_next_job()

            print(f"timepoint: {i}, active jobs:")
            pprint(self.active_jobs)
            print(f"picked job: {picked_job}")
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        print(f"tasks: {self.tasks}")
        print(f"jobs: {self.jobs}")
        print(f"resources: {self.resources}")
        print(f"max timepoint: {self.max_timepoint} \n")
        pass

    @abstractmethod
    def pick_next_job(self) -> Job:
        pass

    def generate_jobs(self) -> list[Job]:
        "This function is used to generate the joblist for the considered timeframe from the task list"
        jobs = []

        for task in self.tasks:
            print(f"\ncreating jobs for task: {task}")

            # TODO check behaviour if division is not round
            num_jobs = int(self.max_timepoint / task.period)
            print(f"number of jobs for task: {num_jobs}")
            
            for i in range(num_jobs):
                jobs.append(Job(name=f"{task.name}_j{i}",arrival_time=(task.start + i * task.period),execution_requirement=task.wcet,deadline=(task.start + i * task.period + task.relative_deadline)))

        print(f"\njobs for taskset: {jobs}\n")
        return jobs
    
    def update_active_jobs(self, current_time) -> None:
        """ 
        A job is active when:
            1: arrival time <= current time
            2: current time <= deadline
            3: the execution requirement was not fulfilled yet
        """
        
        # append currently active jobs
        for job in self.jobs:
            job_is_active = job.arrival_time <= current_time and current_time <= job.deadline and job.execution_requirement > 0

            if job_is_active and job not in self.active_jobs:
                self.active_jobs.append(job)
            elif not job_is_active and job in self.active_jobs:
                self.active_jobs.remove(job) 
