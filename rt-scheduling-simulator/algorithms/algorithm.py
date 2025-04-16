from abc import ABC, abstractmethod

class Algorithm(ABC):
    def __init__(self, tasks, resources, max_timepoint):
        self.tasks = tasks
        self.resources = resources
        self.max_timepoint = max_timepoint
        self.generate_jobs()

    @abstractmethod
    def calculate(self) -> None:
        """This function performs the algorithm calculation"""
        pass
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        print(f"tasks: {self.tasks}")
        print(f"resources: {self.resources}")
        print(f"max timepoint: {self.max_timepoint} \n")
        pass

    def generate_jobs(self) -> None:
        "This function is used to generate the joblist for the considered timeframe from the task list"
        jobs = []

        for task in self.tasks:
            print(f"creating jobs for task: {task}")
            period = int(task["period"])
            wcet = int(task["wcet"])
            start = int(task["start"])
            deadline = int(task["deadline"])

            # TODO check behaviour if division is not round
            num_jobs = int(self.max_timepoint / period)
            print(num_jobs)
            
            for i in range(num_jobs):
                jobs.append({"arrival_time": (start + i * period), "execution_requirement": wcet, "deadline": (start + i * period + deadline)})

            print(jobs)
        pass