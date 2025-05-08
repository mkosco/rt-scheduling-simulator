import os
import sys
import json
import math
import uuid
from rt_scheduling_simulator.algorithms.algorithm import Algorithm
from rt_scheduling_simulator.algorithms.edf import EDF
from rt_scheduling_simulator.algorithms.llf import LLF
from rt_scheduling_simulator.algorithms.mllf import MLLF
from rt_scheduling_simulator.algorithms.rms import RMS
from rt_scheduling_simulator.algorithms.fps import FPS
from rt_scheduling_simulator.model.task import Task

MAX_SIMULATION_TIME = 10000

def pick_algorithm(algorithm_name: str, tasks: list[Task], resources: list, max_timepoint: int) -> Algorithm:
    if algorithm_name.lower() == "edf":
        return EDF(tasks, resources, max_timepoint)
    elif algorithm_name.lower() == "llf":
        return LLF(tasks, resources, max_timepoint)
    elif algorithm_name.lower() == "mllf":
        return MLLF(tasks, resources, max_timepoint)
    elif algorithm_name.lower() == "rms":
        return RMS(tasks, resources, max_timepoint)
    elif algorithm_name.lower() == "fps":
        return FPS(tasks, resources, max_timepoint)
    else:
        # Default to EDF if algorithm not recognized
        print(f"Algorithm {algorithm_name} not recognized, using EDF")
        return EDF(tasks, resources, max_timepoint)
        
def main():
    if len(sys.argv) != 2:
        print("Usage: python simulation_runner.py <filename>")
        sys.exit(1)

    # Access the single argument
    argument = sys.argv[1]
    print(f"Simulation called with argument: {argument}")

    try:
        with open(argument, 'r') as file:
            data = json.load(file)
            algorithm_name: str = data["algorithm"]
            raw_tasks = data["tasks"]
            tasks: list[Task] = []
            resources = data["resources"]

            # parse raw dict tasks into task dataclass
            for task in raw_tasks: 
                # TODO set fps priority
                tasks.append(Task(name=task["name"],start=int(task["start"]),wcet=int(task["wcet"]),period=int(task["period"]),relative_deadline=int(task["deadline"]), fps_priority=int(task["fps_priority"])))

            # TODO parse raw resources into resource dataclass

            print(f"JSON content successfully loaded: {data}")

            task_starting_points: list[int] = [task.start for task in tasks]
            print(f"aggregated task starting points: {task_starting_points}")

            task_periods: list[int] = [task.period for task in tasks]
            print(f"aggregated task periods: {task_periods}")

            # TODO check whether this is correct
            max_timepoint = min(max(task_starting_points) + math.lcm(*task_periods), MAX_SIMULATION_TIME)
            print(f"max simulation timepoint: {max_timepoint}")

            # create simulation result file
            folder_path = os.path.join(os.getcwd(), 'data/sim_result_files')
            print(f"folder path for sim result file storage: {folder_path}")
            
            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path for the JSON file
            save_path = os.path.join(folder_path, f"rt-scheduling-simulator-result_{uuid.uuid4()}.json")
            print(f"folder path for the created sim result file: {save_path}")

            algorithm = pick_algorithm(algorithm_name, tasks=tasks, resources=resources, max_timepoint=max_timepoint)

            algorithm.summarize()

            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                data["result"] = algorithm.calculate()

                json.dump(data, json_file, indent=4)

    except FileNotFoundError:
        print(f"Error: File '{argument}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{argument}' is not a valid JSON file.")
        sys.exit(1)


if __name__ == "__main__":
    main()