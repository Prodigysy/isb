import json
import logging
import os

from file_utils import read_json_file, read_text_file, write_text_file


logging.basicConfig(level=logging.INFO)


def analyze_character_frequency(input_file_path: str, output_file_path: str) -> None:
    """
    Analyzes the frequency of characters in the text file specified by input_file_path 
    and saves the results in a JSON file specified by output_file_path.

    Args:
        input_file_path (str): The path to the input text file.
        output_file_path (str): The path to save the output JSON file.

    Returns:
        None
    """
    try:
        input_text = read_text_file(input_file_path)
        
        if not input_text:
            logging.warning("Input file is empty.")
            return
        
        char_count = {}
        total_chars = 0
        for char in input_text:
            if char.strip():
                char_count[char] = char_count.get(char, 0) + 1
                total_chars += 1
        
        char_freq_percentage = {
            char: count / total_chars * 100 for char, count in char_count.items()}
        sorted_char_frequency = dict(sorted(
            char_freq_percentage.items(), key=lambda item: item[1], reverse=True))
        
        write_text_file(output_file_path, sorted_char_frequency)
        
        logging.info(
            "Character frequency analysis results (sorted by frequency and represented as percentages) saved to JSON file successfully.")
    except FileNotFoundError as e:
        logging.error(f"The input file '{input_file_path}' was not found.")
    except PermissionError as e:
        logging.error(f"Permission denied to access the file: {e}")
    except Exception as e:
        logging.error(f"An error occurred during character frequency analysis: {e}")


def replace_keys_in_text(input_path: str, output_path: str, key_path: str) -> None:
    """
    Replace keys in the text file with their corresponding values from a JSON file.

    Args:
        input_path (str): The path to the input text file.
        output_path (str): The path to save the output text file.
        key_path (str): The path to the JSON file containing the key-value mapping.

    Returns:
        None
    """
    try:
        input_text = read_text_file(input_path)
        key_mapping = read_json_file(key_path)

        for key, value in key_mapping.items():
            input_text = input_text.replace(key, value)

        write_text_file(output_path, input_text)

        logging.info("Keys replaced with their corresponding values and saved to file successfully.")

    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"The input file '{input_path}' or key file '{key_path}' was not found or permission denied: {e}")
    except Exception as e:
        logging.error(f"An error occurred during key replacement: {e}")


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
        analyze_character_frequency(config_params['input_file'], 
                           config_params['output_file'])
        replace_keys_in_text(config_params['json_file'], 
                                 config_params['input_file'], 
                                 config_params['output_file2'])
    except FileNotFoundError as e:
        logging.error(f"The options file '{e.filename}' was not found.")
    except PermissionError as e:
        logging.error(f"Permission denied to access the file: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

