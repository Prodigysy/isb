import enum
import logging

from cryptography.hazmat.primitives import asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


logging.basicConfig(level=logging.INFO)


class Action(enum.Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


def rsa_encrypt_decrypt(key, symmetric_key, action):
    """
    Encrypts or decrypts the symmetric key using the RSA public key or private key.
    
    Parameters:
        key (asymmetric.RSAPublicKey or asymmetric.RSAPrivateKey): The RSA public key for encryption or private key for decryption.
        symmetric_key (bytes): The symmetric key to be encrypted or decrypted.
        action (Action): The action to perform - Action.ENCRYPT or Action.DECRYPT.
    
    Returns:
        bytes: The encrypted or decrypted data.
    """
    match action:
        case Action.ENCRYPT:
            logging.debug("Encrypting symmetric key.")
            encrypted_data = key.encrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.debug(f"Encrypted data: {encrypted_data}")
            return encrypted_data
        case Action.DECRYPT:
            logging.debug("Decrypting symmetric key.")
            decrypted_data = key.decrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.debug(f"Decrypted data: {decrypted_data}")
            return decrypted_data
        case _:
            logging.error("Invalid action. Use Action.ENCRYPT or Action.DECRYPT.")
            raise ValueError("Invalid action. Use Action.ENCRYPT or Action.DECRYPT.")

