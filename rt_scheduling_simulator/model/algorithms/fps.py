from rt_scheduling_simulator.model.algorithms.algorithm import Algorithm 
from rt_scheduling_simulator.model.job import Job, JobState
from rt_scheduling_simulator.logging import debug_print
from rt_scheduling_simulator.model.protocol import Protocol

class FPS(Algorithm):
    def summarize(self):
        debug_print(f"\nFPS")
        super().summarize()
        pass

    """ 
    This is FPS so we sort according to the highest priority 
    One is the highets priority, higher integers mean a lower priority
    """
    def sort_jobs(self) -> list[Job]:
        # TODO adjust this so it takes whatever is bigger fps_priority or protocol priority
        return [job for job in sorted(self.active_jobs, key=lambda job: job.fps_priority)]
    
    def upate_resource_assignments(self, sorted_jobs) -> None:
        super().upate_resource_assignments(sorted_jobs)
    
        # this is the pip workflow 
        
        # should pip be active 
        if self.protocol is Protocol.PIP:
            # find jobs that have a locked resource that is needed by a higher prio job
            # check blocked jobs 
            blocked_jobs = [job for job in self.active_jobs if job.state is JobState.BLOCKED]
            for job in blocked_jobs:
                if job.resources_needed is not None:
                    
                    # get a list of jobs that hold resources the current job needs
                    jobs_holding_needed_resources: list[Job] = []
                    for resource in job.resources_needed:
                        job_with_resource = self.resource_to_job.get(resource.name)
                        if job_with_resource is not None:
                            jobs_holding_needed_resources.append(job_with_resource)
                    
                    """
                    raise the priority of the jobs that hold resources the currently selected blocked job needs
                    if the currently blocked job has a higher prioritys
                    """
                    for job_holding_needed_resource in jobs_holding_needed_resources:
                        if max(job_holding_needed_resource.fps_priority, job_holding_needed_resource.protocol_priority) < max(job.protocol_priority, job.fps_priority):
                            job_holding_needed_resource.protocol_priority = job.fps_priority
                    
                # check wether there is a high prio job that needs a resource of a lower prio job 
                
                # if that is the case increase the prio of the lower prio job
