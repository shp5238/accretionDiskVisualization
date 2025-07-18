import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', help='Path to the directory containing .txt files')
    args = parser.parse_args()

    file_list = [os.path.join(args.data_dir, f) for f in os.listdir(args.data_dir) if f.endswith(".txt")]
    
    if not file_list:
        print("No .txt files found.")
        return

    if len(file_list) == 1:
        print("Found 1 text file.")
    else:
        print(f"Found {len(file_list)} text files.")

    print("Program completed successfully!")

if __name__ == "__main__":
    main()

