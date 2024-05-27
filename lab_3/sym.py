import enum
import logging

from cryptography.hazmat.primitives import asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


logging.basicConfig(level=logging.INFO)


class Action(enum.Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"

def rsa_encrypt_decrypt(key, data, action):
    match action:
        case Action.ENCRYPT:
            logging.debug("Encrypting data.")
            encrypted_data = key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.debug(f"Data encrypted: {encrypted_data}")
            return encrypted_data
        case Action.DECRYPT:
            logging.debug("Decrypting data.")
            decrypted_data = key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.debug(f"Data decrypted: {decrypted_data}")
            return decrypted_data
        case _:
            raise ValueError("Invalid action specified for encryption/decryption.")
