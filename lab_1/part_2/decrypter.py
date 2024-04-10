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
