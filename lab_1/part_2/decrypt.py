import os
import json
import logging
from collections import Counter
from file_utils import read_text_file, write_text_file, read_json_file


logging.basicConfig(level=logging.INFO)


def frequency_analysis(input_file: str, output_file: str) -> None:
    """
    Perform frequency analysis on the characters in the input file and write the results to the output file.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.

    Returns:
        None
    """
    try:
        original_text = read_json_file(input_file)
        character_count = Counter(original_text)
        total_characters = sum(character_count.values())
        character_frequency_percentage = {
            char: count / total_characters * 100 for char, count in character_count.items()}
        sorted_character_frequency = dict(sorted(
            character_frequency_percentage.items(), key=lambda item: item[1], reverse=True))
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_character_frequency, f,
                      ensure_ascii=False, indent=4)
        logging.info(
            "Frequency analysis results (sorted by frequency and represented as percentages) written to JSON file successfully.")
    except FileNotFoundError as e:
        logging.error(f"The input file '{input_file}' was not found.")
    except PermissionError as e:
        logging.error(f"Permission denied to access the file: {e}")
    except Exception as e:
        logging.error(f"An error occurred during frequency analysis: {e}")

def replace_keys_with_values(json_file: str, input_file: str, output_file: str) -> None:
    """
    Replace keys in the input text file with their corresponding values from the JSON file
    and write the modified text to the output file.

    Args:
        json_file (str): Path to the JSON file containing key-value pairs.
        input_file (str): Path to the input text file.
        output_file (str): Path to the output text file.

    Returns:
        None
    """
    try:
        json_data = read_json_file(json_file)
        original_text = read_text_file(input_file)
        for key, value in json_data.items():
            original_text = original_text.replace(key, value)
        write_text_file(output_file, original_text)
        logging.info(
            "Replacement completed successfully. Results written to the output file.")
    except FileNotFoundError as e:
        logging.error(f"The file '{e.filename}' was not found.")
    except PermissionError as e:
        logging.error(f"Permission denied to access the file: {e}")
    except Exception as e:
        logging.error(
            f"An error occurred during replacement: {e}")

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
        config_params = read_json_file(os.path.join("lab_1", "options_2.json"))
        frequency_analysis(config_params['input_file'], 
                           config_params['output_file'])
        replace_keys_with_values(config_params['json_file'], 
                                 config_params['input_file'], 
                                 config_params['output_file2'])
    except FileNotFoundError as e:
        logging.error(f"The options file '{e.filename}' was not found.")
    except PermissionError as e:
        logging.error(f"Permission denied to access the file: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

