import os


def validate_token(token, length):
    if len(token) == length:
        return True
    return False


def validate_path(path):
    if os.path.exists(path):
        return True
    return False


def validate_extension(path, extension):
    if path.endswith(extension):
        return True
    return False


def file_exists(path):
    return os.path.isfile(path)
