import random
import json
import zipfile
from pathlib import Path


def generate_random_key(length):
    """
    Generate a random key of specified length.

    Args:
        length (int): The length of the key.

    Returns:
        str: The generated key.
    """
    all_characters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя0123456789!:;'
    shuffled_characters = random.sample(all_characters, len(all_characters))
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
    with filepath.open('w', encoding='utf-8') as file:
        json.dump(key_dict, file, ensure_ascii=False)


def vigenere_cipher(text, key, mode):
    """
    Encrypts or decrypts text using the Vigenere cipher.

    Args:
        text (str): The original text.
        key (str): The encryption or decryption key.
        mode (str): The mode, 'encrypt' for encryption or 'decrypt' for decryption.

    Returns:
        str: The encrypted or decrypted text.
    """
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('а')
            if mode == 'decrypt':
                shift = -shift
            shifted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
            result += shifted_char
            key_index += 1
        else:
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
    with open(file_path, 'r', encoding='utf-8') as file:
        all_text = file.read()
        sentences = all_text.split('.')
        start_index = random.randint(0, len(sentences) - num_sentences)
        excerpt = '. '.join(sentences[start_index:start_index + num_sentences]) + '.'
        return excerpt


def process_texts(file_path, action, keys):
    """
    Processes texts with the specified action (encryption or decryption).

    Args:
        file_path (str): The path to the text file.
        action (str): The action, 'encrypt' for encryption or 'decrypt' for decryption.
        keys (list): The list of keys.

    Returns:
        None
    """
    with zipfile.ZipFile("encrypted_texts_and_keys.zip", "w") as zip_file:
        for i in range(100):
            text_excerpt = get_random_text_excerpt(file_path)

            if action == 'encrypt':
                processed_text = vigenere_cipher(text_excerpt, keys[i], 'encrypt')
            elif action == 'decrypt':
                processed_text = vigenere_cipher(text_excerpt, keys[i], 'decrypt')

            zip_file.writestr(f"original_text_{i+1}.txt", text_excerpt)
            zip_file.writestr(f"{action}_text_{i+1}.txt", processed_text)


file_path = "C:\\Users\\user\\Desktop\\isb-main\\isb\\lab_1\\part_2\\master_i_margarita.txt"
keys = [generate_random_key(random.randint(5, 10)) for _ in range(100)]
decrypt_keys = [generate_random_key(random.randint(5, 10)) for _ in range(100)]

process_texts(file_path, 'encrypt', keys)
save_keys_to_json(keys, decrypt_keys, "keys.json")
process_texts(file_path, 'decrypt', decrypt_keys)
