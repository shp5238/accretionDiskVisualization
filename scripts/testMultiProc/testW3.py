# testW3.py
import sys
import os

def run_program(file_path, radius):
    with open(file_path, "r") as f:
        value = int(f.readline())
    # Logging to stderr so stdout is clean
    #print(f"Processed {file_path} with radius {radius}, value: {value}", file=sys.stderr)
    #print(f"PID is {os.getpid()}", file=sys.stderr)

    #print(f"Processed {file_path} with radius {radius}, value: {value}, PID: {os.getpid()}", file=sys.stderr)
    
    print(f"Processed {file_path} with radius {radius}, value: {value}, PID: {os.getpid()}")
    # Output value (clean)
    print(value)

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: python testW3.py <radius> <file>", file=sys.stderr)
        sys.exit(1)
    radius = int(args[0])
    file_path = args[1]
    run_program(file_path, radius)

if __name__ == "__main__":
    main()

