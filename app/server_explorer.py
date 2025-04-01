import os

def list_files():
    for root, dirs, files in os.walk("."):
        for file in files:
            print(os.path.join(root, file))

if __name__ == "__main__":
    list_files()
