import os
import json
import logging

logging.basicConfig(level=logging.INFO)


def caesar_cipher_decoder(input_path: str, output_path: str, shift: int, key_path: str) -> None:
    """
    Decodes the contents of the input file using a Caesar cipher with a specified shift value,
    then saves the decoded text to an output file.
    
    Args:
        input_path (str): The path to the input file containing the text to be decoded.
        output_path (str): The path to the output file where the decoded text will be saved.
        shift (int): The number of positions used for encoding the text.
        key_path (str): The path to the JSON file containing the encoding key.
    
    Returns:
        None
    """

    try:
        if not 1 <= shift <= 31:
            raise ValueError("Shift must be in the range from 1 to 31")

        if not os.access(input_path, os.R_OK):
            raise FileNotFoundError(f"Input file '{input_path}' is not accessible")
        if not os.access(os.path.dirname(output_path), os.W_OK):
            raise FileNotFoundError(f"Output directory '{os.path.dirname(output_path)}' is not writable")
        if not os.access(os.path.dirname(key_path), os.R_OK):
            raise FileNotFoundError(f"Key file directory '{os.path.dirname(key_path)}' is not accessible")

        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        with open(key_path, 'r', encoding='utf-8') as json_file:
            encoding_dict = json.load(json_file)

        decoded_text = ""
        for char in text:
            if char in encoding_dict.values():
                original_char = [k for k, v in encoding_dict.items() if v == char][0]
                base_char = 'а' if original_char.islower() else 'А'
                decoded_char = chr((ord(original_char) - ord(base_char) - shift) % 32 + ord(base_char))
                decoded_text += decoded_char
            else:
                decoded_text += char

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(decoded_text)

    except ValueError as ve:
        logging.error(f"Invalid value: {str(ve)}")
    except FileNotFoundError as fe:
        logging.error(str(fe))
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    try:
        with open(os.path.join("lab_1", "part_1", "options_2.json"), 'r', encoding='utf-8') as json_file:
            params = json.load(json_file)
        
        input_path = params.get("input")
        output_path = params.get("output")
        shift = params.get("shift")
        key_path = params.get("key")
        
        if input_path and isinstance(input_path, str) and \
           output_path and isinstance(output_path, str) and \
           key_path and isinstance(key_path, str) and \
           isinstance(shift, int):

            caesar_cipher_decoder(input_path, output_path, shift, key_path)
        else:
            logging.error("Invalid parameters in options_2.json")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
