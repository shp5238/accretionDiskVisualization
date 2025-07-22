import sys

# Define a Worker class or just use plain functions — up to you.
class Worker:
    values = []
    count = 0

    @staticmethod
    def run_program(file_path, radius):
        with open(file_path, "r") as f:
            Worker.values.append(int(f.readline()))
            Worker.count += 1
        return (f"Processed {file_path} with radius {radius}")

def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print("Usage: python testWorker.py <radius> <file>")
        sys.exit(1)

    radius = args[0]
    file_path = args[1]

    print(f"Running with radius: {radius}")
    print(f"Processing file: {file_path}")

    Worker.run_program(file_path, radius)

    # Optional: show state at the end
    print(f"Worker.values: {Worker.values}")
    print(f"Worker.count: {Worker.count}")

if __name__ == '__main__':
    main()
