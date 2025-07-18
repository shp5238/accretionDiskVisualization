import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='Path to the directory containing .athdf files')
    args = parser.parse_args()

    file_list = [os.path.join(args.data_dir, f) for f in os.listdir(args.data_dir) if f.endswith(".athdf")]
    
    if not file_list:
        print("No .athdf files found.")
        print(f"in the folder {args.data_dir}")
        return

    if len(file_list) == 1:
        print("Found 1 athdf file.")
    else:
        print(f"Found {len(file_list)} athdf files.")

    print("Program completed successfully!")

if __name__ == "__main__":
    main()

