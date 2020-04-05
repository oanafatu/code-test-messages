import os


def get_file_path(caller_path, relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(caller_path)), relative_path)