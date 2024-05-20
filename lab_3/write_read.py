import logging

logging.basicConfig(level=logging.INFO)

def write_data(path, data):
    """
    Function for writing data in a file.
    
    Parameters:
        path (str): Path where the file is located.
        data (bytes): Data to be recorded.
    """
    try:
        with open(path, 'wb') as file:
            file.write(data)
        logging.info(f"Data has been written to {path}")
    except Exception as e:
        logging.error(f"Failed to write data to {path}: {e}")

def read_file(path):
    """
    Function for reading files.
    
    Parameters:
        path (str): Path where the file is located.
    
    Returns:
        bytes: Data read from the file.
    """
    try:
        with open(path, 'rb') as file:
            data = file.read()
        logging.info(f"Data has been read from {path}")
        return data
    except Exception as e:
        logging.error(f"Failed to read data from {path}: {e}")
        return None
