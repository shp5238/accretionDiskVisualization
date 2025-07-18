from concurrent.futures import ProcessPoolExecutor
import os

def main():
	num_cores = os.cpu_count() or 1 # Fallback to 1 if undetectable
	print(f"There are {num_cores} cores.")
	return

if __name__ == "__main__":
	main()
