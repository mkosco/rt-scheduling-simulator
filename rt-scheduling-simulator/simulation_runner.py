import os
import sys
import json
import math
import uuid
from algorithms.edf import EDF

MAX_SIMULATION_TIME = 10000

if len(sys.argv) != 2:
    print("Usage: python simulation_runner.py <filename>")
    sys.exit(1)

# Access the single argument
argument = sys.argv[1]
print(f"Simulation called with argument: {argument}")

try:
    with open(argument, 'r') as file:
        data = json.load(file)
        tasks = data["tasks"]
        resources = data["resources"]

        print(f"JSON content successfully loaded: {data}")

        task_starting_points: list[int] = [int(task["start"]) for task in tasks]
        print(f"aggregated task starting points: {task_starting_points}")

        task_periods: list[int] = [int(task["period"]) for task in tasks]
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

        algorithm = EDF(tasks, resources, max_timepoint)

        algorithm.summarize()

        # Save the JSON data to the file
        with open(save_path, 'w') as json_file:
            data["result"] = {"timeline": []}

            algorithm.calculate()

            json.dump(data, json_file, indent=4)

except FileNotFoundError:
    print(f"Error: File '{argument}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File '{argument}' is not a valid JSON file.")
    sys.exit(1)