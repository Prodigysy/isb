import logging

from asymmetric_crypto import AsymmetricCrypto
from symmetric_crypto import SymmetricCrypto

import file_utils


logging.basicConfig(level=logging.INFO)


class CryptographySystem:
    def __init__(self, symmetric_key_path, public_key_path, private_key_path, rsa_key_size, sym_key_size_bits, algorithm):
        """
        Initialize the CryptographySystem class.

        :param symmetric_key_path: Path to save the symmetric key.
        :param public_key_path: Path to save the public key.
        :param private_key_path: Path to save the private key.
        :param rsa_key_size: Size of the RSA key in bits.
        :param sym_key_size_bits: Size of the symmetric key in bits.
        :param algorithm: Symmetric encryption algorithm to use.
        """
        self.symmetric_key_path = symmetric_key_path
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path
        self.rsa_key_size = rsa_key_size
        self.sym_key_size_bits = sym_key_size_bits
        self.algorithm = algorithm

        self.asymmetric_crypto = AsymmetricCrypto(rsa_key_size)
        self.symmetric_crypto = SymmetricCrypto(sym_key_size_bits, algorithm)

    def key_generation(self):
        """
        Generate and save symmetric and asymmetric keys.
        """
        # Generate and save symmetric key
        sym_key = self.symmetric_crypto.generate_key()
        file_utils.save_key(sym_key, self.symmetric_key_path)
        logging.info(f"Symmetric key saved to {self.symmetric_key_path}")

        # Generate and save RSA keys
        private_key, public_key = self.asymmetric_crypto.generate_keys()
        self.asymmetric_crypto.save_private_key(self.private_key_path)
        self.asymmetric_crypto.save_public_key(self.public_key_path)
        logging.info(f"Private key saved to {self.private_key_path}")
        logging.info(f"Public key saved to {self.public_key_path}")

    def encrypt_file(self, input_file_path, output_file_path):
        """
        Encrypt a file using both symmetric and asymmetric encryption.

        :param input_file_path: Path to the input file to be encrypted.
        :param output_file_path: Path to save the encrypted file.
        """
        # Load data from input file
        data = file_utils.load_file(input_file_path)

        # Encrypt data with symmetric key
        encrypted_data = self.symmetric_crypto.encrypt(data)

        # Load public key
        self.asymmetric_crypto.load_public_key(self.public_key_path)

        # Encrypt symmetric key with public key
        encrypted_sym_key = self.asymmetric_crypto.encrypt(self.symmetric_crypto.key)

        # Save encrypted symmetric key and encrypted data
        with open(output_file_path, 'wb') as f:
            f.write(encrypted_sym_key + b"|||" + encrypted_data)
        logging.info(f"File encrypted and saved to {output_file_path}")

    def decrypt_file(self, input_file_path, output_file_path):
        """
        Decrypt a file using both symmetric and asymmetric decryption.

        :param input_file_path: Path to the encrypted input file.
        :param output_file_path: Path to save the decrypted file.
        """
        # Load encrypted data from input file
        with open(input_file_path, 'rb') as f:
            encrypted_sym_key, encrypted_data = f.read().split(b"|||")

        # Load private key
        self.asymmetric_crypto.load_private_key(self.private_key_path)

        # Decrypt symmetric key with private key
        decrypted_sym_key = self.asymmetric_crypto.decrypt(encrypted_sym_key)

        # Set the decrypted symmetric key
        self.symmetric_crypto.key = decrypted_sym_key

        # Decrypt data with symmetric key
        decrypted_data = self.symmetric_crypto.decrypt(encrypted_data)

        # Save decrypted data to output file
        file_utils.save_file(decrypted_data, output_file_path)
        logging.info(f"File decrypted and saved to {output_file_path}")
