import os
import json
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)


class CipherMode(Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


def caesar_cipher(input_text: str, shift: int, mode: CipherMode) -> str:
    """
    Perform Caesar cipher encryption or decryption on the input text.

    Args:
        input_text (str): The text to be encrypted or decrypted.
        shift (int): The number of positions to shift each alphabetic character in the text.
        mode (CipherMode): The mode of operation (encrypt or decrypt).

    Returns:
        str: The encrypted or decrypted text.
    """
    output_text = ""
    for char in input_text:
        if char.isalpha():
            base_char = 'a' if char.islower() else 'A'
            shifted_char = chr((ord(char) - ord(base_char) + shift) % 26 + ord(base_char))
            output_text += shifted_char
        else:
            output_text += char
    return output_text


def check_file_access(file_path: str, mode: str) -> None:
    """
    Check if the file exists and has the specified access mode.

    Args:
        file_path (str): The path to the file.
        mode (str): The access mode to check ('r' for read, 'w' for write).

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file does not have the required access mode.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found")

    if not os.access(file_path, mode):
        raise PermissionError(f"No {mode} permission for file '{file_path}'")


def caesar_cipher_encoder(input_path: str, output_path: str, shift: int, key_path: str, mode: CipherMode) -> None:
    """
    Encrypts or decrypts the contents of the input file using a Caesar cipher with a specified shift value,
    then saves the result to an output file and the encoding key to a JSON file.

    Args:
        input_path (str): The path to the input file containing the text to be processed.
        output_path (str): The path to the output file where the processed text will be saved.
        shift (int): The number of positions to shift each alphabetic character in the text.
        key_path (str): The path to the output file where the encoding key will be saved in JSON format.
        mode (CipherMode): The mode of operation (encrypt or decrypt).

    Returns:
        None
    """

    try:
        match mode:
            case CipherMode.ENCRYPT:
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be in the range from 1 to 25")

                check_file_access(input_path, 'r')
                check_file_access(os.path.dirname(output_path), 'w')
                check_file_access(os.path.dirname(key_path), 'w')

            case CipherMode.DECRYPT:
                if not 1 <= shift <= 25:
                    raise ValueError("Shift must be in the range from 1 to 25")

                check_file_access(input_path, 'r')
                check_file_access(os.path.dirname(output_path), 'w')
                check_file_access(os.path.dirname(key_path), 'w')

        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        if mode == CipherMode.ENCRYPT:
            processed_text = caesar_cipher(text, shift, CipherMode.ENCRYPT)
        elif mode == CipherMode.DECRYPT:
            processed_text = caesar_cipher(text, shift, CipherMode.DECRYPT)
        else:
            raise ValueError("Invalid mode. Mode must be 'encrypt' or 'decrypt'.")

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)

        if mode == CipherMode.ENCRYPT:
            encoding_dict = {char: caesar_cipher(char, shift, CipherMode.ENCRYPT) for char in text}
        else:
            encoding_dict = {caesar_cipher(char, shift, CipherMode.ENCRYPT): char for char in text}

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
        with open(os.path.join("lab_1", "part_1", "options_1.json"), 'r', encoding='utf-8') as json_file:
            params = json.load(json_file)
        
        input_path = params.get("input")
        output_path = params.get("output")
        shift = params.get("shift")
        key_path = params.get("key")
        mode_str = params.get("mode")

        if input_path and isinstance(input_path, str) and \
           output_path and isinstance(output_path, str) and \
           key_path and isinstance(key_path, str) and \
           isinstance(shift, int) and mode_str and isinstance(mode_str, str):

            mode = CipherMode(mode_str)
            caesar_cipher_encoder(input_path, output_path, shift, key_path, mode)
        else:
            logging.error("Invalid parameters in options_1.json")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
