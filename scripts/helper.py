import os

def get_directory():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, '../data')
    return path

def get_filename(filename):
    path = get_directory()
    path = os.path.join(path, filename)
    return path

