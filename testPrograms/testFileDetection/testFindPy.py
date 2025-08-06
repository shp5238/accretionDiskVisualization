import os


def find_proj_root(marker_name):
    curr = os.path.abspath(os.path.dirname(os.getcwd()))    

    while True: 
        # looks for file or directory
        if os.path.isdir(os.path.join(curr, marker_name)) or os.path.isfile(os.path.join(curr, marker_name)):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr: # Reached filesystem root 
            print(parent)
            raise FileNotFoundError(f"Could not fiind marker: {marker_name}.")
        curr = parent

def main():
    # code here
    root = find_proj_root('dummy.txt')
    print(root)
    


if __name__ == "__main__":
    main()
