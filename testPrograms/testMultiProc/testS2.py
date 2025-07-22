# testS2.py

import sys
import argparse
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import partial

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

# --- Worker Runner ---
def run_worker_script(file_path, radius):
    # Build and run: python testW2.py <radius> <file>
    result = subprocess.run(
        [sys.executable, 'testW2.py', str(radius), file_path],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="Usage: python3 testScript.py <radius>")
    parser.add_argument("radius", type=radial_int)
    args = parser.parse_args()

    # Discover files
    file_list = ["t0.txt", "t1.txt", "t2.txt", "t3.txt"]

    # Partial function to bind fixed radius
    worker_fn = partial(run_worker_script, radius=args.radius)

    # Run in parallel using subprocess workers
    with ProcessPoolExecutor() as executor:
        results = executor.map(worker_fn, file_list)
        for result in results:
            print(result)

if __name__ == "__main__":
    main()

