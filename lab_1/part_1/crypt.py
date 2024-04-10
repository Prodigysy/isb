import os
import json
import logging

logging.basicConfig(level=logging.INFO)


def caesar_cipher_encoder(input_path: str, output_path: str, shift: int, key_path: str) -> None:
    """
    Encodes the contents of the input file using a Caesar cipher with a specified shift value,
    then saves the encoded text to an output file and the encoding key to a JSON file.
    
    Args:
        input_path (str): The path to the input file containing the text to be encoded.
        output_path (str): The path to the output file where the encoded text will be saved.
        shift (int): The number of positions to shift each alphabetic character in the text.
        key_path (str): The path to the output file where the encoding key will be saved in JSON format.
    
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
        if not os.access(os.path.dirname(key_path), os.W_OK):
            raise FileNotFoundError(f"Key file directory '{os.path.dirname(key_path)}' is not writable")

        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        encoded_text = ""
        encoding_dict = {}

        for char in text:
            if char.isalpha():
                base_char = 'а' if char.islower() else 'А'
                encoded_char = chr((ord(char) - ord(base_char) + shift) % 32 + ord(base_char))
                encoded_text += encoded_char
                encoding_dict[char] = encoded_char
            else:
                encoded_text += char

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(encoded_text)

        with open(key_path, 'w', encoding='utf-8') as json_file:
            json.dump(encoding_dict, json_file, ensure_ascii=False)

    except ValueError as ve:
        logging.error(f"Invalid value: {str(ve)}")
    except FileNotFoundError as fe:
        logging.error(str(fe))
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    try:
        with open(os.path.join("lab_1","part_1","options_1.json"), 'r', encoding='utf-8') as json_file:
            params = json.load(json_file)
        
        input_path = params.get("input")
        output_path = params.get("output")
        shift = params.get("shift")
        key_path = params.get("key")
        
        if input_path and isinstance(input_path, str) and \
           output_path and isinstance(output_path, str) and \
           key_path and isinstance(key_path, str) and \
           isinstance(shift, int):

            caesar_cipher_encoder(input_path, output_path, shift, key_path)
        else:
            logging.error("Invalid parameters in options_1.json")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
