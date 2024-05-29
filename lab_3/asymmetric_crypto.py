import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


logging.basicConfig(level=logging.INFO)


class AsymmetricCrypto:
    def __init__(self, rsa_key_size):
        """
        Initialize the AsymmetricCrypto class.

        :param rsa_key_size: Size of the RSA key in bits.
        """
        self.rsa_key_size = rsa_key_size
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """
        Generate a pair of RSA keys (private and public).

        :return: Tuple containing the private key and public key.
        """
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=self.rsa_key_size)
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key

    def save_private_key(self, path):
        """
        Save the private key to a file.

        :param path: Path to the file where the private key will be saved.
        """
        private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(path, 'wb') as f:
            f.write(private_key_pem)

    def save_public_key(self, path):
        """
        Save the public key to a file.

        :param path: Path to the file where the public key will be saved.
        """
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(path, 'wb') as f:
            f.write(public_key_pem)

    def load_private_key(self, path):
        """
        Load a private key from a file.

        :param path: Path to the file from which the private key will be loaded.
        """
        with open(path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)

    def load_public_key(self, path):
        """
        Load a public key from a file.

        :param path: Path to the file from which the public key will be loaded.
        """
        with open(path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(f.read())

    def encrypt(self, data):
        """
        Encrypt data using the public key.

        :param data: Data to be encrypted.
        :return: Encrypted data.
        """
        return self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, data):
        """
        Decrypt data using the private key.

        :param data: Data to be decrypted.
        :return: Decrypted data.
        """
        return self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
