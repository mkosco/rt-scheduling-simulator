import os
import sys
import json
import math
import uuid
import rt_scheduling_simulator
from rt_scheduling_simulator.logging import DEBUG, debug_print
from rt_scheduling_simulator.algorithms.algorithm import Algorithm
from rt_scheduling_simulator.algorithms.edf import EDF
from rt_scheduling_simulator.algorithms.llf import LLF
from rt_scheduling_simulator.algorithms.mllf import MLLF
from rt_scheduling_simulator.algorithms.rms import RMS
from rt_scheduling_simulator.algorithms.fps import FPS
import rt_scheduling_simulator.logging
from rt_scheduling_simulator.model.task import Task

MAX_SIMULATION_TIME = 10000

def pick_algorithm(algorithm_name: str, tasks: list[Task], resources: list, assignments: list, max_timepoint: int) -> Algorithm:
    if algorithm_name.lower() == "edf":
        return EDF(tasks, resources, assignments, max_timepoint)
    elif algorithm_name.lower() == "llf":
        return LLF(tasks, resources, assignments, max_timepoint)
    elif algorithm_name.lower() == "mllf":
        return MLLF(tasks, resources, assignments, max_timepoint)
    elif algorithm_name.lower() == "rms":
        return RMS(tasks, resources, assignments, max_timepoint)
    elif algorithm_name.lower() == "fps":
        return FPS(tasks, resources, assignments, max_timepoint)
    else:
        # Default to EDF if algorithm not recognized
        debug_print(f"Algorithm {algorithm_name} not recognized, using EDF")
        return EDF(tasks, resources, assignments, max_timepoint)

def main():
    global DEBUG

    if "--debug" in sys.argv:
        rt_scheduling_simulator.logging.DEBUG = True
        sys.argv.remove("--debug")

    if len(sys.argv) != 2:
        debug_print("Usage: python simulation_runner.py <filename> [--debug]")
        sys.exit(1)

    argument = sys.argv[1]
    debug_print(f"Simulation called with argument: {argument}")
    
    try:
        with open(argument, 'r') as file:
            data = json.load(file)
            algorithm_name: str = data["algorithm"]
            raw_tasks = data["tasks"]
            raw_resources = data["resources"]
            raw_asssignments = data["assignments"]
            tasks: list[Task] = []

            debug_print(f"raw assignments: {raw_asssignments}")

            # parse raw dict tasks into task dataclass
            for task in raw_tasks: 
                fps_priority = int(task["fps_priority"]) if task["fps_priority"] else None
                tasks.append(Task(name=task["name"],start=int(task["start"]),wcet=int(task["wcet"]),period=int(task["period"]),relative_deadline=int(task["deadline"]), fps_priority=fps_priority))

            # TODO parse raw resources into resource dataclass

            debug_print(f"JSON content successfully loaded: {data}")

            task_starting_points: list[int] = [task.start for task in tasks]
            debug_print(f"aggregated task starting points: {task_starting_points}")

            task_periods: list[int] = [task.period for task in tasks]
            debug_print(f"aggregated task periods: {task_periods}")

            # TODO check whether this is correct
            max_timepoint = min(max(task_starting_points) + math.lcm(*task_periods), MAX_SIMULATION_TIME)
            debug_print(f"max simulation timepoint: {max_timepoint}")

            # create simulation result file
            folder_path = os.path.join(os.getcwd(), 'data/sim_result_files')
            debug_print(f"folder path for sim result file storage: {folder_path}")
            
            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path for the JSON file
            result_id = uuid.uuid4()
            save_path = os.path.join(folder_path, f"rt-scheduling-simulator-result_{result_id}.json")
            debug_print(f"folder path for the created sim result file: {save_path}")

            algorithm = pick_algorithm(algorithm_name, tasks=tasks, resources=raw_resources, assignments=raw_asssignments, max_timepoint=max_timepoint)

            algorithm.summarize()

            # Save the JSON data to the file
            with open(save_path, 'w') as json_file:
                data["result"] = algorithm.calculate()

                json.dump(data, json_file, indent=4)
                
            print(result_id)

    except FileNotFoundError:
        debug_print(f"Error: File '{argument}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        debug_print(f"Error: File '{argument}' is not a valid JSON file.")
        sys.exit(1)


if __name__ == "__main__":
    main()