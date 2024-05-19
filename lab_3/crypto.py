import os
import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from write_read import write_data, read_file
from sym import encrypt_decrypt, Action


logging.basicConfig(level=logging.INFO)

class Cryptography:
    """Class of hybrid cryptosystem. Symmetric Triple Des encryption algorithm, Asymmetric RSA.
    Methods:
        1. key_generation(self) -> None
        2. encryption(self, text_file_path: str, encryption_file_path: str) -> None
        3. decryption(self, encryption_file_path: str, decryption_file_path: str) -> None
    """

    def __init__(self):
        self.key_size = 2048  # RSA key size
        self.symmetric_key_size = 24  # 24 bytes for 3DES key
        self.symmetric_key = os.urandom(self.symmetric_key_size)
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=self.key_size)
        self.public_key = self.private_key.public_key()

    def key_generation(self) -> None:
        """Generates RSA public and private keys."""
        # Save the private key
        private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        write_data("private_key.pem", private_key_pem)

        # Save the public key
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        write_data("public_key.pem", public_key_pem)

        logging.info("RSA keys generated and saved.")

    def encryption(self, text_file_path: str, encryption_file_path: str) -> None:
        """Encrypts a file using hybrid encryption."""
        # Read the plaintext file
        plaintext = read_file(text_file_path)

        # Encrypt the plaintext using the symmetric key (3DES)
        encrypted_text = encrypt_decrypt(self.symmetric_key, plaintext, Action.ENCRYPT)

        # Encrypt the symmetric key using the RSA public key
        encrypted_symmetric_key = self.public_key.encrypt(
            self.symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Write the encrypted symmetric key and the encrypted text to a file
        write_data(encryption_file_path, encrypted_symmetric_key + encrypted_text)
        logging.info(f"File encrypted and saved to {encryption_file_path}")

    def decryption(self, encryption_file_path: str, decryption_file_path: str) -> None:
        """Decrypts a file using hybrid decryption."""
        # Read the encrypted file
        encrypted_data = read_file(encryption_file_path)
        
        # Extract the encrypted symmetric key and the encrypted text
        encrypted_symmetric_key = encrypted_data[:256]  # RSA 2048-bit key size
        encrypted_text = encrypted_data[256:]

        # Decrypt the symmetric key using the RSA private key
        self.symmetric_key = self.private_key.decrypt(
            encrypted_symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypt the encrypted text using the symmetric key (3DES)
        decrypted_text = encrypt_decrypt(self.symmetric_key, encrypted_text, Action.DECRYPT)

        # Write the decrypted text to the output file
        write_data(decryption_file_path, decrypted_text)
        logging.info(f"File decrypted and saved to {decryption_file_path}")

if __name__ == "__main__":
    # Example usage
    crypto_system = Cryptography()
    
    # Generate RSA keys
    crypto_system.key_generation()
    
    # Encrypt a file
    crypto_system.encryption('example.txt', 'encrypted.bin')
    
    # Decrypt the file
    crypto_system.decryption('encrypted.bin', 'decrypted.txt')
