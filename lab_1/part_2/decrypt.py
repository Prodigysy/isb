import os
import logging
from file_utils import read_text_file, write_text_file, read_json_file


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
        encoded_text = read_text_file(input_path)
        key_mapping = read_json_file(key_path)

        decoded_text = encoded_text
        for encoded_char, decoded_char in key_mapping.items():
            decoded_text = decoded_text.replace(decoded_char, encoded_char)

        write_text_file(output_path, decoded_text)

    except Exception as e:
        logging.error(f"An unexpected error occurred during file processing: {e}")


if __name__ == '__main__':
    try:
        config_params = read_json_file(os.path.join("lab_1", "part_2", "options_2.json"))
        decode_text(config_params["input_file"], config_params["output_file"], config_params["key"])
    except Exception as e:
        logging.error(f"An error occurred: {e}")
