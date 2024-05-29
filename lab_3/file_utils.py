import os

def save_key(key, path):
    """
    Save a key to a file.

    :param key: Key to be saved.
    :param path: Path to the file where the key will be saved.
    """
    with open(path, 'wb') as f:
        f.write(key)

def load_key(path):
    """
    Load a key from a file.

    :param path: Path to the file from which the key will be loaded.
    :return: Loaded key.
    """
    with open(path, 'rb') as f:
        return f.read()

def save_file(data, path):
    """
    Save data to a file.

    :param data: Data to be saved.
    :param path: Path to the file where the data will be saved.
    """
    with open(path, 'wb') as f:
        f.write(data)

def load_file(path):
    """
    Load data from a file.

    :param path: Path to the file from which the data will be loaded.
    :return: Loaded data.
    """
    with open(path, 'rb') as f:
        return f.read()
