import os
import sys
import Miner


# Checks if the user passed 3 arguments (the Startup.py file, the dataset path, and their GitHub access token).
def validate_args(args):
    if len(args) == 3:
        return True
    return False


# Checks if the file exists.
def validate_path(path):
    if os.path.exists(path):
        return True
    return False


# Checks if the file extension is valid.
def validate_extension(path):
    if path.endswith('.json'):
        return True
    return False


# Checks if the access token is valid, as it must be 40 characters in length.
def validate_token(token):
    if len(token) == 40:
        return True
    return False


# Program execution
def main():
    if not validate_args(sys.argv):
        print("The path to the dataset and your personal access token must be passed as arguments:\n"
              "'python Startup.py <path> <token>'")
        return

    path = sys.argv[1]
    token = sys.argv[2]

    if not validate_path(path):
        print("Invalid path - file not found")
        return

    if not validate_extension(path):
        print("Incorrect file extension - must be a JSON file")
        return

    if not validate_token(token):
        print("Invalid access token - must be 40 characters in length")
        return

    Miner.mine(path, token)


# Program initialisation
if __name__ == "__main__":
    main()
