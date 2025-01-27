import os

def read_file(filepath):
    """
    Reads the contents of a file.

    :param filepath: The path to the file.
    :return: The contents of the file as a string.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filepath, content):
    """
    Writes content to a file.

    :param filepath: The path to the file.
    :param content: The content to write.
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def ensure_directory(directory):
    """
    Ensures that a directory exists.

    :param directory: The path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
