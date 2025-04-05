import sys
import json

if len(sys.argv) != 2:
    print("Usage: python simulation_runner.py <filename>")
    sys.exit(1)

# Access the single argument
argument = sys.argv[1]
print(f"Simulation called with argument: {argument}")

try:
    with open(argument, 'r') as file:
        data = json.load(file)
        print("JSON content successfully loaded:")
        print(data)

        # find timepoint where all possible combinations have been found: Timepoint = max(Start_A, Start_B, Start_C) + LCM(Period_A, Period_B, Period_C)

except FileNotFoundError:
    print(f"Error: File '{argument}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File '{argument}' is not a valid JSON file.")
    sys.exit(1)