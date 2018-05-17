import os

root_path = ''


def get_root():
    root_path = os.path.abspath('')
    root_path = root_path.replace("\\", "/")
    return root_path