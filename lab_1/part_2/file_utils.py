import json
import logging


def read_text_file(file_path: str) -> str:
    """
    Read the contents of a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The contents of the text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        return ""
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the text file: {e}")
        return ""


def read_json_file(file_path: str) -> dict:
    """
    Read the contents of a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in file: {e}")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the JSON file: {e}")
        return {}


def write_text_file(file_path: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        file_path (str): The path to the text file.
        content (str): The content to write to the file.

    Returns:
        None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to the text file: {e}")


def write_json_file(file_path: str, data: dict) -> None:
    """
    Write data to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (dict): The data to write to the file.

    Returns:
        None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to the JSON file: {e}")
