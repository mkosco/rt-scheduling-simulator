from abc import ABC, abstractmethod
from dataclasses import asdict
from rt_scheduling_simulator.logging import debug_pprint, debug_print
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.model.task import Task 

class Algorithm(ABC):
    def __init__(self, tasks: list[Task], resources, assignments, max_timepoint):
        self.tasks = tasks
        self.resources = resources
        self.assignments = assignments
        self.max_timepoint = max_timepoint
        self.jobs = self.generate_jobs()
        self.active_jobs: list[Job] = []
        self.result = {}
        self.result["summary"] = []
        self.result["timeline"] = []
        self.current_time = 0
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        debug_print(f"tasks: {self.tasks}")
        debug_print(f"jobs: ")
        debug_pprint(self.jobs)
        debug_print(f"resources: {self.resources}")
        debug_print(f"assignments: {self.assignments}")
        debug_print(f"max timepoint: {self.max_timepoint} \n")

    @abstractmethod
    def pick_next_job(self) -> Job:
        pass

    def calculate(self) -> dict:
        """This function performs the algorithm calculation"""
        i = 0
        while True:
            self.current_time = i
            self.update_active_jobs(i)
            
            if not self.active_jobs:
                return self.result
            
            debug_print(f"timepoint: {i}, active jobs:")
            debug_pprint(self.active_jobs)

            picked_job = self.pick_next_job()
            debug_print(f"picked job: {picked_job}")

            active_job_copy = list(map(asdict, self.active_jobs))
            self.result["timeline"].append({'timepoint' : i, 'active_jobs' : active_job_copy})

            picked_job.execution_requirement -= 1
            i += 1

    # TODO refactor out 
    def generate_jobs(self) -> list[Job]:
        "This function is used to generate the joblist for the considered timeframe from the task list"
        jobs = []
        
        # TODO this isn't very nice as all the jobs get rms priorities, even when not using rms
        
        # sort according to smallest period
        self.tasks.sort(key=lambda task: task.period)
        rms_priority = 1
        prev_period = self.tasks[0].period

        for task in self.tasks:
            debug_print(f"\ncreating jobs for task: {task}")

            # one is the highest priority
            if task.period > prev_period:
                rms_priority += 1

            # TODO check behaviour if division is not round
            num_jobs = int(self.max_timepoint / task.period)
            debug_print(f"number of jobs for task: {num_jobs}")
            
            for i in range(num_jobs):
                jobs.append(Job(name=f"{task.name.strip()}_j{i}",
                                arrival_time=(task.start + i * task.period),
                                execution_requirement=task.wcet,
                                deadline=(task.start + i * task.period + task.relative_deadline),
                                state=JobState.INACTIVE,
                                laxity=None,
                                resources=[],
                                fps_priority=task.fps_priority,
                                rms_priority=rms_priority))

        debug_print(f"\njobs for taskset:\n")
        debug_pprint(jobs)
        return jobs
    
    # TODO refactor out
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
                job.state = JobState.FINNISHED

                if job.execution_requirement > 0:
                    job.state = JobState.MISSED
                    debug_print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n unfinished job: {job}")
                self.result["summary"].append(asdict(job))
                self.active_jobs.remove(job) 
