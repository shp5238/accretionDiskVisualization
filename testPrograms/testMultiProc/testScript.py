# testScript.py

import os
import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial

# --- Validation Helper ---
def radial_int(value):
    len_r = 512
    try:
        fvalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid int.")

    if not (-len_r <= fvalue <= len_r - 1):
        raise argparse.ArgumentTypeError(
            f"{fvalue} is out of bounds. Radius must be between -{len_r} and {len_r - 1}."
        )
    return fvalue

# --- Core Worker ---
class Worker:
    values = []
    count = 0

    @staticmethod
    def run_program(file_path, radius):
        with open(file_path, "r") as f:
            value = int(f.readline())
            Worker.values.append(value)
            Worker.count += 1
            print(f"Processed {file_path} with radius {radius}, value: {value}")

# --- Main Controller ---
def main():
    parser = argparse.ArgumentParser(
        description="Format: python testScript.py <radius>"
    )
    parser.add_argument(
        "radius", type=radial_int,
        help="Integer radius index between -512 and 511"
    )

    args = parser.parse_args()

    # Discover files
    file_list = ["t0.txt", "t1.txt", "t2.txt", "t3.txt"]

    # Create a partial function to bind the radius argument
    worker_fn = partial(Worker.run_program, radius=args.radius)

    # Run multiprocessing
    num_cores = 10  # You can also use: os.cpu_count()
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = executor.map(worker_fn, file_list)
        for r in results:
           print(r)

if __name__ == "__main__":
    main()

