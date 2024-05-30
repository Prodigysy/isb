import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

logging.basicConfig(level=logging.INFO)

class SymmetricCrypto:
    def __init__(self, key_size_bits: int, algorithm: str) -> None:
        """
        Initialize the SymmetricCrypto class.

        :param key_size_bits: Size of the symmetric key in bits.
        :param algorithm: Symmetric encryption algorithm to use.
        """
        self.key_size_bits = key_size_bits
        self.algorithm = algorithm
        self.key = self.generate_key()

    def generate_key(self) -> bytes:
        """
        Generate a symmetric key based on the specified key size.

        :return: Generated symmetric key.
        """
        key_size_bytes = self.key_size_bits // 8
        if self.algorithm == "Blowfish":
            if 32 <= self.key_size_bits <= 448 and self.key_size_bits % 8 == 0:
                return os.urandom(key_size_bytes)
            else:
                raise ValueError("Invalid key size for Blowfish. Choose a size between 32 and 448 bits, in multiples of 8.")
        match self.key_size_bits:
            case 64:
                if self.algorithm == "3DES":
                    return os.urandom(key_size_bytes)
                else:
                    raise ValueError("Invalid key size for the selected algorithm.")
            case 128:
                return os.urandom(key_size_bytes)
            case 192:
                if self.algorithm in ["3DES", "Camellia"]:
                    return os.urandom(key_size_bytes)
                else:
                    raise ValueError("Invalid key size for the selected algorithm.")
            case 256:
                if self.algorithm in ["Camellia", "ChaCha20"]:
                    return os.urandom(key_size_bytes)
                else:
                    raise ValueError("Invalid key size for the selected algorithm.")
            case _:
                raise ValueError("Invalid symmetric key size.")

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data using the symmetric key and specified algorithm.

        :param data: Data to be encrypted.
        :return: Encrypted data.
        """
        cipher = self._get_cipher()
        encryptor = cipher.encryptor()
        if self.algorithm in ["3DES", "Camellia", "Blowfish"]:
            padder = sym_padding.PKCS7(cipher.algorithm.block_size).padder()
            padded_data = padder.update(data) + padder.finalize()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        elif self.algorithm == "ChaCha20":
            nonce = os.urandom(16)
            encrypted_data = nonce + encryptor.update(data) + encryptor.finalize()
        else:
            raise ValueError("Unsupported algorithm.")
        return encrypted_data

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt data using the symmetric key and specified algorithm.

        :param data: Data to be decrypted.
        :return: Decrypted data.
        """
        cipher = self._get_cipher(data[:16]) if self.algorithm == "ChaCha20" else self._get_cipher()
        decryptor = cipher.decryptor()
        if self.algorithm == "ChaCha20":
            data = data[16:]
        decrypted_padded_data = decryptor.update(data) + decryptor.finalize()
        if self.algorithm in ["3DES", "Camellia", "Blowfish"]:
            unpadder = sym_padding.PKCS7(cipher.algorithm.block_size).unpadder()
            decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
            return decrypted_data
        return decrypted_padded_data

    def _get_cipher(self, nonce: bytes = None) -> Cipher:
        """
        Get the cipher object for the specified algorithm.

        :param nonce: Nonce value for ChaCha20 (optional).
        :return: Cipher object.
        """
        match self.algorithm:
            case "3DES":
                return Cipher(algorithms.TripleDES(self.key), modes.ECB())
            case "Camellia":
                return Cipher(algorithms.Camellia(self.key), modes.ECB())
            case "Blowfish":
                return Cipher(algorithms.Blowfish(self.key), modes.ECB())
            case "ChaCha20":
                if nonce is None:
                    nonce = os.urandom(16)
                return Cipher(algorithms.ChaCha20(self.key, nonce), mode=None)
            case _:
                raise ValueError("Invalid encryption algorithm. Choose '3DES', 'Camellia', 'Blowfish', or 'ChaCha20'.")
