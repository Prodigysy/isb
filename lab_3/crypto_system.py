import os
import logging

from cryptography.hazmat.primitives import serialization, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Cryptography:
    """Class of hybrid cryptosystem. Symmetric Triple DES encryption algorithm, Asymmetric RSA.
    Methods:
        1. key_generation(self) -> None
        2. encryption(self, text_file_path: str, encryption_file_path: str) -> None
        3. decryption(self, encryption_file_path: str, decryption_file_path: str) -> None
    """

    def __init__(self, symmetric_key_path: str, public_key_path: str, private_key_path: str, rsa_key_size: int, sym_key_size_bits: int):
        self.symmetric_key_path = symmetric_key_path
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path
        self.rsa_key_size = rsa_key_size  
        self.sym_key_size_bits = sym_key_size_bits
        self.symmetric_key = None
        self.private_key = None
        self.public_key = None


    def generate_symmetric_key(self):
        """Generates a symmetric key of the specified size in bits."""
        if self.sym_key_size_bits == 64:
            return os.urandom(8)
        elif self.sym_key_size_bits == 128:
            return os.urandom(16)
        elif self.sym_key_size_bits == 192:
            return os.urandom(24)
        else:
            raise ValueError("Invalid symmetric key size. Choose 64, 128, or 192 bits.")
        

    def key_generation(self) -> None:
        """Generates RSA public and private keys and a symmetric key."""
        try:
            self.symmetric_key = self.generate_symmetric_key()
            self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=self.rsa_key_size)
            self.public_key = self.private_key.public_key()

            private_key_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(self.private_key_path, 'wb') as f:
                f.write(private_key_pem)

            public_key_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(self.public_key_path, 'wb') as f:
                f.write(public_key_pem)

            with open(self.symmetric_key_path, 'wb') as f:
                f.write(self.symmetric_key)

            logging.info("RSA keys and symmetric key generated and saved.")
        except Exception as e:
            logging.error(f"Ошибка при генерации ключей: {e}")


    def encryption(self, text_file_path: str, encryption_file_path: str) -> None:
        """Encrypts a file using hybrid encryption."""
        try:
            with open(text_file_path, 'rb') as f:
                plaintext = f.read()
            logging.info(f"Data has been read from {text_file_path}")

            encrypted_symmetric_key = self.public_key.encrypt(
                self.symmetric_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            logging.debug(f"Encrypted symmetric key length: {len(encrypted_symmetric_key)}")

            encrypted_text = self._encrypt_decrypt(self.symmetric_key, plaintext, 'encrypt')

            logging.debug(f"Encrypted text length: {len(encrypted_text)}")

            with open(encryption_file_path, 'wb') as f:
                f.write(encrypted_symmetric_key + encrypted_text)
            logging.info(f"Data encrypted and saved to {encryption_file_path}")
        except Exception as e:
            logging.error(f"Ошибка при шифровании текста: {e}")


    def decryption(self, encryption_file_path: str, decryption_file_path: str) -> None:
        """Decrypts a file using hybrid encryption."""
        try:
            with open(encryption_file_path, 'rb') as f:
                encrypted_data = f.read()
            logging.info(f"Data has been read from {encryption_file_path}")

            encrypted_symmetric_key = encrypted_data[:self.rsa_key_size // 8]
            encrypted_text = encrypted_data[self.rsa_key_size // 8:]

            logging.debug(f"Encrypted symmetric key length: {len(encrypted_symmetric_key)}")
            logging.debug(f"Encrypted text length: {len(encrypted_text)}")

            symmetric_key = self.private_key.decrypt(
                encrypted_symmetric_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            decrypted_text = self._encrypt_decrypt(symmetric_key, encrypted_text, 'decrypt')

            with open(decryption_file_path, 'wb') as f:
                f.write(decrypted_text)
            logging.info(f"File decrypted and saved to {decryption_file_path}")
        except Exception as e:
            logging.error(f"Ошибка при расшифровании текста: {e}")


    def _encrypt_decrypt(self, key, data, action):
        try:
            cipher = Cipher(algorithms.TripleDES(key), modes.ECB())
            if action == 'encrypt':
                encryptor = cipher.encryptor()
                padder = sym_padding.PKCS7(algorithms.TripleDES.block_size).padder()
                padded_data = padder.update(data) + padder.finalize()
                encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
                return encrypted_data
            elif action == 'decrypt':
                decryptor = cipher.decryptor()
                decrypted_padded_data = decryptor.update(data) + decryptor.finalize()
                unpadder = sym_padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
                decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
                return decrypted_data
            else:
                raise ValueError("Invalid action. Use 'encrypt' or 'decrypt'.")
        except Exception as e:
            logging.error(f"Ошибка при {action} данных: {e}")
