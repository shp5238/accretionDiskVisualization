# testS3.py
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
"""
def run_worker_script(file_path, radius):
    result = subprocess.run(
        [sys.executable, 'testW3.py', str(radius), file_path],
        capture_output=True, text=True
    )
    output = result.stdout.strip()
    try:
        return int(output)
    except ValueError:
        print(f"Unexpected output for {file_path}: {output}", file=sys.stderr)
        return 0  # or raise Exception if you want to fail
"""
def run_worker_script(file_path, radius):
    result = subprocess.run(
        [sys.executable, 'testW3.py', str(radius), file_path],
        capture_output=True, text=True
    )

    # Print the entire stdout for debugging
    print(f"[{file_path} STDOUT]:\n{result.stdout.strip()}")
    if result.stderr:
        print(f"[{file_path} STDERR]:\n{result.stderr.strip()}", file=sys.stderr)

    # Extract last line from stdout (should be the numeric value)
    output_lines = result.stdout.strip().splitlines()
    if not output_lines:
        print(f"Empty output from {file_path}", file=sys.stderr)
        return 0

    last_line = output_lines[-1]  # This should be the number
    try:
        return int(last_line)
    except ValueError:
        print(f"Invalid numeric output from {file_path}: {last_line}", file=sys.stderr)
        return 0



def main():
    parser = argparse.ArgumentParser(description="Usage: python3 testS2.py <radius>")
    parser.add_argument("radius", type=radial_int)
    args = parser.parse_args()

    file_list = ["t0.txt", "t1.txt", "t2.txt", "t3.txt"]

    worker_fn = partial(run_worker_script, radius=args.radius)

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(worker_fn, file_list))
        for r in results:
            print(f"Got value: {r}")
        avg = sum(results) / len(results)
        print(f"\nThe average value is {avg:.2f}")

if __name__ == "__main__":
    main()

