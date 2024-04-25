import random
import os
import json
import zipfile
import logging

from typing import List
from pathlib import Path
from enum import Enum


logging.basicConfig(level=logging.INFO)


ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя0123456789!:;'

class CipherMode(Enum):
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'


def generate_random_key(length):
    """
    Generate a random key of specified length.

    Args:
        length (int): The length of the key.

    Returns:
        str: The generated key.
    """
    shuffled_characters = random.sample(ALPHABET, len(ALPHABET))
    return ''.join(shuffled_characters[:length])


def save_keys_to_json(keys, decrypt_keys, filename):
    """
    Save keys as a JSON file.

    Args:
        keys (list): The list of encryption keys.
        decrypt_keys (list): The list of decryption keys.
        filename (str): The name of the JSON file.

    Returns:
        None
    """
    key_dict = {keys[i]: decrypt_keys[i] for i in range(len(keys))}
    filepath = Path(filename)
    try:
        with filepath.open('w', encoding='utf-8') as file:
            json.dump(key_dict, file, ensure_ascii=False)
    except Exception as e:
        logging.error(f"An error occurred while saving the keys to JSON file: {e}")


def vigenere_cipher(text, key, mode: CipherMode):
    """
    Encrypts or decrypts text using the Vigenere cipher.

    Args:
        text (str): The original text.
        key (str): The encryption or decryption key.
        mode (CipherMode): The mode, CipherMode.ENCRYPT for encryption or CipherMode.DECRYPT for decryption.

    Returns:
        str: The encrypted or decrypted text.
    """
    result = ""
    key_index = 0
    for char in text:
        case = mode
        shift = ord(key[key_index % len(key)]) - ord('а')
        match case:
            case CipherMode.ENCRYPT:
                if char.isalpha():
                    shifted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
                else:
                    shifted_char = char
                result += shifted_char
                key_index += 1
            case CipherMode.DECRYPT:
                if char.isalpha():
                    shift = -shift
                    shifted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
                else:
                    shifted_char = char
                result += shifted_char
                key_index += 1
            case _:
                result += char
    return result



def get_random_text_excerpt(file_path, num_sentences=5):
    """
    Retrieves a random excerpt from a file with a specified number of sentences.

    Args:
        file_path (str): The path to the text file.
        num_sentences (int): The number of sentences in the excerpt.

    Returns:
        str: The random text excerpt.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            all_text = file.read()
            sentences = all_text.split('.')
            start_index = random.randint(0, len(sentences) - num_sentences)
            excerpt = '. '.join(sentences[start_index:start_index + num_sentences]) + '.'
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def process_texts(file_path, action, keys):
    """
    Processes texts with the specified action (encryption or decryption).

    Args:
        file_path (str): The path to the text file.
        action (CipherMode): The action, CipherMode.ENCRYPT for encryption or CipherMode.DECRYPT for decryption.
        keys (list): The list of keys.

    Returns:
        None
    """
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
        zip_filename = settings.get('zip_filename', 'encrypted_texts_and_keys.zip')
        num_texts = settings.get('num_texts', 100)
        num_sentences = settings.get('num_sentences', 5)

    try:
        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            for i in range(num_texts):
                text_excerpt = get_random_text_excerpt(file_path, num_sentences)

                processed_text = vigenere_cipher(text_excerpt, keys[i], action)

                zip_file.writestr(f"original_text_{i+1}.txt", text_excerpt)
                zip_file.writestr(f"{action.value}_text_{i+1}.txt", processed_text)
    except Exception as e:
        logging.error(f"An error occurred while processing texts: {e}")



if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "master_i_margarita.txt")

    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
        num_keys = settings.get("num_keys", 100)
        min_key_length = settings.get("min_key_length", 5)
        max_key_length = settings.get("max_key_length", 10)

    keys = [generate_random_key(random.randint(min_key_length, max_key_length)) for _ in range(num_keys)]
    decrypt_keys = [generate_random_key(random.randint(min_key_length, max_key_length)) for _ in range(num_keys)]

    process_texts(file_path, CipherMode.ENCRYPT, keys)
    save_keys_to_json(keys, decrypt_keys, "keys.json")
    process_texts(file_path, CipherMode.DECRYPT, decrypt_keys)

