# testW2.py

import sys
import os

def run_program(file_path, radius):
    with open(file_path, "r") as f:
        value = int(f.readline())
    print(f"Processed {file_path} with radius {radius}, value: {value}")
    print(f"PID is {os.getpid()}")

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: python testW2.py <radius> <file>")
        sys.exit(1)
    radius = int(args[0])
    file_path = args[1]
    run_program(file_path, radius)

if __name__ == "__main__":
    main()

