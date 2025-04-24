from abc import ABC, abstractmethod
from model.job import Job
from model.task import Task 

class Algorithm(ABC):
    def __init__(self, tasks, resources, max_timepoint):
        self.tasks = tasks
        self.resources = resources
        self.max_timepoint = max_timepoint
        self.jobs = self.generate_jobs()
        self.active_jobs = []

    @abstractmethod
    def calculate(self) -> None:
        """This function performs the algorithm calculation"""
        pass
    
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
            period = int(task["period"])
            task_name = task["name"]
            wcet = int(task["wcet"])
            start = int(task["start"])
            deadline = int(task["deadline"])

            # TODO check behaviour if division is not round
            num_jobs = int(self.max_timepoint / period)
            print(f"number of jobs for task: {num_jobs}")
            
            for i in range(num_jobs):
                jobs.append(Job(name=f"{task_name}_j{i}",arrival_time=(start + i * period),execution_requirement=wcet,deadline=(start + i * period + deadline)))

        print(f"\njobs for taskset: {jobs}\n")
        return jobs
    
    def update_active_jobs(self, current_time) -> None:
        """ 
        A job is active when:
            1: arrival time <= current time
            2: current time <= deadline
            3: the execution requirement was not fulfilled yet
        """
        
        for job in self.jobs:
            if job.arrival_time <= current_time and current_time <= job.deadline and job.execution_requirement > 0 and job not in self.active_jobs:
                self.active_jobs.append(job)

        pass