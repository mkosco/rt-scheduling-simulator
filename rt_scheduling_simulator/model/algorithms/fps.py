from queue import Empty
from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.logging import debug_print
from rt_scheduling_simulator.model.protocol import Protocol

class FPS(Algorithm):
    def summarize(self):
        debug_print(f"\nFPS")
        super().summarize()
        pass
    
    # Use a helper to treat None priorities as very low priority (0)
    def effective_priority(self, job: Job) -> int:
        # If either priority is None, treat it as low priority (0).
        fps = job.fps_priority if job.fps_priority is not None else 0
        proto = job.protocol_priority if job.protocol_priority is not None else 0
        return int(max(fps, proto))

    """ 
    This is FPS so we sort according to the highest priority 
    One is the highets priority, higher integers mean a lower priority
    """
    def sort_jobs(self) -> list[Job]:
        return [job for job in sorted(self.active_jobs, key=self.effective_priority, reverse=True)]
    
    def upate_resource_assignments(self, sorted_jobs) -> None:
        super().upate_resource_assignments(sorted_jobs)
        
        # should pip be active 
        if self.protocol == Protocol.PIP:
            # find jobs that have a locked resource that is needed by a higher prio job
            # check blocked jobs 
            blocked_jobs = [job for job in self.active_jobs if job.state is JobState.BLOCKED]
            for job in blocked_jobs:
                if job.resources_needed is not None and job.resources_needed:
                    # get a list of jobs that hold resources the current job needs
                    jobs_holding_needed_resources: list[Job] = []
                    for resource in job.resources_needed:
                        job_with_resource = self.resource_to_job.get(resource.name)
                        if job_with_resource is not None and job_with_resource is not job:
                            jobs_holding_needed_resources.append(job_with_resource)
                    
                    """
                    raise the priority of the jobs that hold resources the currently selected blocked job needs
                    if the currently blocked job has a higher prioritys
                    """
                    for job_holding_needed_resource in jobs_holding_needed_resources:
                        if self.effective_priority(job_holding_needed_resource) < self.effective_priority(job):
                            job_holding_needed_resource.protocol_priority = job.fps_priority if job.fps_priority is not None else job.protocol_priority