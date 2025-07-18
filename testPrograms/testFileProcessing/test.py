import os
import argparse

extra_info = False  # Move global variable to the top for clarity

def process_file(file_path, radius=None):
    if extra_info:
        print(f"Processing {file_path}")
    # TODO: Add computation logic here
    # For example: open the file and do something
    return file_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='Path to the directory containing .athdf files')
    args = parser.parse_args()

    file_list = [os.path.join(args.data_dir, f) for f in os.listdir(args.data_dir) if f.endswith(".athdf")]

    if not file_list:
        print("No .athdf files found.")
        print(f"In the folder: {args.data_dir}")
        return

    if len(file_list) == 1:
        print("Found 1 athdf file.")
    else:
        print(f"Found {len(file_list)} athdf files.")

    print(process_file(file_list[0]))

    print("Program completed successfully!")

if __name__ == "__main__": 
    main()

