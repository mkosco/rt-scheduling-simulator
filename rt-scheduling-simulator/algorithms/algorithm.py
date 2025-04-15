from abc import ABC, abstractmethod

class Algorithm(ABC):
    def __init__(self, tasks, resources):
        self.tasks = tasks
        self.resources = resources

    @abstractmethod
    def calculate(self) -> None:
        """This function performs the algorithm calculation"""
        pass
    
    @abstractmethod
    def summarize(self) -> None:
        """This function prints a sumary of the algorithm and it's initialization"""
        print(f"tasks: {self.tasks}")
        print(f"resources: {self.resources} \n")
        pass