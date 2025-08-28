from abc import ABC, abstractmethod
import copy
from dataclasses import asdict
from typing import Optional
from rt_scheduling_simulator.logging import debug_pprint, debug_print
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.model.protocol import Protocol
from rt_scheduling_simulator.model.task import Task 
from rt_scheduling_simulator.model.assignment import Assignment 
from rt_scheduling_simulator.model.resource import Resource 

class Algorithm(ABC):
    def __init__(self, tasks: list[Task], resources: list[Resource], assignments: list[Assignment], max_timepoint, protocol: Protocol):
        self.tasks = tasks
        self.resources: list[Resource] = resources
        self.assignments = assignments
        self.max_timepoint = max_timepoint
        self.protocol = protocol
        
        # maps job names to assignments for the task that generated the job
        self.job_to_assignments: dict[str, Optional[list[Assignment]]] = {}
        self.resource_to_job: dict[str, Optional[Job]] = {}
        self.jobs: list[Job] = self.generate_jobs()
        self.active_jobs: list[Job] = []
        self.result = {}
        self.result["summary"] = []
        self.result["timeline"] = []
        self.current_time = 0
        
        # initialize resource assignment map empty
        for resource in self.resources:
            self.resource_to_job[resource.name] = None
            
        debug_pprint(self.resource_to_job)
            
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        debug_print(f"tasks: {self.tasks}")
        debug_print(f"protocol: {self.protocol}")
        debug_print(f"jobs: ")
        debug_pprint(self.jobs)
        debug_print(f"resources: {self.resources}")
        debug_print(f"assignments: {self.assignments}")
        debug_print(f"max timepoint: {self.max_timepoint} \n")

    @abstractmethod
    def sort_jobs(self) -> list[Job]:
        pass

    def calculate(self) -> dict:
        """This function performs the algorithm calculation"""
        i = 0
        while True:
            self.current_time = i
    
            self.update_active_jobs(i)
            
            # no more jobs, we are done
            if not self.active_jobs:
                return self.result
            
            debug_print(f"timepoint: {i}, active jobs:")
            debug_pprint(self.active_jobs)
            
            self.update_resources_needed()

            sorted_jobs = self.sort_jobs()
            debug_print(f"sorted jobs: {sorted_jobs}")

            self.upate_resource_assignments(sorted_jobs)
            
            # check for deadlocks, if we catch one we finish
            if all(job.state is JobState.BLOCKED for job in sorted_jobs):
                self.update_result(i)
                return self.result             

            picked_job = None
            
            # "pick" a job that is highest in prio and not blocked
            for job in sorted_jobs:
                if job.state is not JobState.BLOCKED:
                    picked_job = job
                    break

            if picked_job is None:
                raise ValueError("No next Job could be picked! Something went wrong")
            
            picked_job.state = JobState.EXECUTING
            
            self.update_result(i)            

            picked_job.steps_executed += 1
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

            # from the total resource assignments filter out the ones relevant to this task
            assignments_filtered_for_task = [assignment for assignment in self.assignments if assignment.task_name == task.name]
            
            for i in range(num_jobs):
                new_job: Job = Job(name=f"{task.name.strip()}_j{i}",
                                arrival_time=(task.start + i * task.period),
                                execution_requirement=task.wcet,
                                steps_executed=0,
                                deadline=(task.start + i * task.period + task.relative_deadline),
                                state=JobState.INACTIVE,
                                laxity=None,
                                resources_needed=None,
                                fps_priority=task.fps_priority,
                                rms_priority=rms_priority)
                
                jobs.append(new_job)
                
                self.job_to_assignments[new_job.name] = copy.deepcopy(assignments_filtered_for_task)

        debug_print(f"\n\njobs for taskset:")
        debug_pprint(jobs)
        debug_print(f"\n\njobs to assignments map:")
        debug_pprint(self.job_to_assignments)
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
            job_is_active = job.arrival_time <= current_time and current_time <= job.deadline and job.steps_executed < job.execution_requirement

            if job_is_active and job not in self.active_jobs:
                job.state = JobState.WAITING
                self.active_jobs.append(job)
            elif not job_is_active and job in self.active_jobs:
                job.state = JobState.FINNISHED  

                if job.steps_executed != job.execution_requirement:
                    job.state = JobState.MISSED
                    debug_print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n unfinished job: {job}")
                
                self.result["summary"].append(asdict(job))
                self.active_jobs.remove(job)
                                                 
    def update_resources_needed(self) -> None:
        """
        This function updates the resources_needed field of the Job Dataclass
        this field tells us which resources the job needs to perform its next execution step
        """
        
        for job in self.active_jobs:
            job.resources_needed = []
            for assignment in self.job_to_assignments.get(job.name):

                if job.steps_executed >= assignment.start and job.steps_executed <= assignment.end:
                    # as the assignment only stores the resource name we need to fetch the obj. matching
                    resources = [r for r in self.resources if r.name == assignment.resource_name]
                    
                    if len(resources) != 1:
                        raise ValueError("No exact match for the resource name was found!")
                    
                    resource = resources[0]
                    
                    job.resources_needed.append(resource)

    def upate_resource_assignments(self, sorted_jobs) -> None: 
        """
        This function iterates over the active jobs 
        when a job is active and needs a resource it
        tries to assign this resource
        """
        
        # free resources that are not needed anymore or belong to jobs that are no longer active
        for resource_name, assigned_job in self.resource_to_job.items():
            if assigned_job is not None and (resource_name not in [resource.name for resource in assigned_job.resources_needed] or assigned_job not in sorted_jobs):
                self.resource_to_job[resource_name] = None

        # assign needed resources
        for job in sorted_jobs:
            if job.resources_needed is not None:
                for resource in job.resources_needed:
                    if self.resource_to_job[resource.name] is None:
                        self.resource_to_job[resource.name] = job
                    elif self.resource_to_job[resource.name] is not job: 
                        job.state = JobState.BLOCKED
                        
        debug_pprint(self.resource_to_job)
        
    def update_result(self, timepoint) -> None:
        active_job_copy = list(map(asdict, self.active_jobs))
        resource_to_job_serialized = {
            resource: asdict(job) if job is not None else None
            for resource, job in copy.deepcopy(self.resource_to_job).items()
        }            
        self.result["timeline"].append({'timepoint' : timepoint, 'active_jobs' : active_job_copy, 'resource_to_job' : resource_to_job_serialized})
