import os
import json
import logging


logging.basicConfig(level=logging.INFO)


def decode_text(input_path: str, output_path: str, key_path: str) -> None:
    """
    Decode the text in the input file using a provided key mapping and save the result to the output file.

    Args:
    - input_path (str): The path to the input file containing the text with encoded letters.
    - output_path (str): The path to the output file where the decoded text will be saved.
    - key_path (str): The path to the JSON file containing the key mapping for letter replacement.

    Returns:
    - None
    """
    
    try:
        
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Key file '{key_path}' not found")
        if not os.access(key_path, os.R_OK):
            raise PermissionError(f"No read permission for key file '{key_path}'")
        
        with open(input_path, 'r', encoding='utf-8') as file:
            encoded_text = file.read()
        
        with open(key_path, 'r', encoding='utf-8') as key_file:
            key_mapping = json.load(key_file)

        decoded_text = encoded_text
        for encoded_char, decoded_char in key_mapping.items():
            decoded_text = decoded_text.replace(decoded_char, encoded_char)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(decoded_text)

    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in key file: {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during file processing: {e}")


if __name__ == '__main__':
    with open(os.path.join("lab_1", "part_2", "options_2.json"), 'r', encoding='utf-8') as json_file:
        config_params = json.load(json_file)
    
    decode_text(config_params["input_file"], config_params["output_file"], config_params["key"])
