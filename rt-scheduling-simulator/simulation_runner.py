import sys

if len(sys.argv) != 2:
    print("Usage: python simulation_runner.py <filename>")
    sys.exit(1)

# Access the single argument
argument = sys.argv[1]
print(f"Simulation called with argument: {argument}")