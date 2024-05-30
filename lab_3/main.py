import sys
import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QMessageBox, QComboBox, QFileDialog,
    QVBoxLayout, QWidget, QLabel, QHBoxLayout
)

from crypto_system import CryptographySystem
from file_utils import load_key

logging.basicConfig(level=logging.INFO)

class CryptoApp(QMainWindow):
    def __init__(self) -> None:
        """
        Initialize the CryptoApp class.
        """
        super().__init__()

        self.setWindowTitle("Система шифрования с помощью TripleDes")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        key_size_layout = QHBoxLayout()
        self.key_size_label = QLabel("Выберите размер ключа RSA:")
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItem("2048")
        self.key_size_combo.addItem("4096")
        key_size_layout.addWidget(self.key_size_label)
        key_size_layout.addWidget(self.key_size_combo)
        layout.addLayout(key_size_layout)

        sym_key_size_layout = QHBoxLayout()
        self.sym_key_size_label = QLabel("Выберите размер симметричного ключа (бит):")
        self.sym_key_size_combo = QComboBox()
        self.sym_key_size_combo.addItem("64")
        self.sym_key_size_combo.addItem("128")
        self.sym_key_size_combo.addItem("192")
        self.sym_key_size_combo.addItem("256")
        self.sym_key_size_combo.addItem("448")
        sym_key_size_layout.addWidget(self.sym_key_size_label)
        sym_key_size_layout.addWidget(self.sym_key_size_combo)
        layout.addLayout(sym_key_size_layout)

        algorithm_layout = QHBoxLayout()
        self.algorithm_label = QLabel("Выберите алгоритм шифрования:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItem("3DES")
        self.algorithm_combo.addItem("Camellia")
        self.algorithm_combo.addItem("Blowfish")
        self.algorithm_combo.addItem("ChaCha20")
        algorithm_layout.addWidget(self.algorithm_label)
        algorithm_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algorithm_layout)

        self.load_keys_button = QPushButton("Загрузить пользовательские ключи")
        self.load_keys_button.clicked.connect(self.load_keys)
        layout.addWidget(self.load_keys_button)

        self.generate_keys_button = QPushButton("Сгенерировать ключи")
        self.generate_keys_button.clicked.connect(self.generate_keys)
        layout.addWidget(self.generate_keys_button)

        self.encryption_button = QPushButton("Зашифровать текст")
        self.encryption_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encryption_button)

        self.decryption_button = QPushButton("Расшифровать текст")
        self.decryption_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decryption_button)

        self.exit_button = QPushButton("Выйти из программы")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.cryptography: Optional[CryptographySystem] = None

    def get_file_path(self, prompt: str) -> str:
        """
        Open a file dialog to select a file.

        :param prompt: Prompt message for the file dialog.
        :return: Selected file path.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, prompt, "", "All Files (*)")
        return file_path

    def save_file_path(self, prompt: str) -> str:
        """
        Open a file dialog to save a file.

        :param prompt: Prompt message for the file dialog.
        :return: Selected file path.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, prompt, "", "All Files (*)")
        return file_path

    def load_keys(self) -> None:
        """
        Load user-provided keys.
        """
        symmetric_key_path: str = self.get_file_path("Выберите файл с симметричным ключом")
        public_key_path: str = self.get_file_path("Выберите файл с публичным ключом")
        private_key_path: str = self.get_file_path("Выберите файл с приватным ключом")

        try:
            symmetric_key: bytes = load_key(symmetric_key_path)
            public_key: bytes = load_key(public_key_path)
            private_key: bytes = load_key(private_key_path)

            rsa_key_size: int = int(self.key_size_combo.currentText())
            sym_key_size: int = int(self.sym_key_size_combo.currentText())
            algorithm: str = self.algorithm_combo.currentText()

            self.cryptography = CryptographySystem(symmetric_key, public_key, private_key, rsa_key_size,
                                                   sym_key_size, algorithm)
            QMessageBox.information(self, "Success", "Пользовательские ключи успешно загружены.")
        except Exception as ex:
            logging.error(f"Ошибка при загрузке пользовательских ключей: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при загрузке пользовательских ключей: {ex}")

    def generate_keys(self) -> None:
        """
        Generate cryptographic keys.
        """
        rsa_key_size: int = int(self.key_size_combo.currentText())
        sym_key_size: int = int(self.sym_key_size_combo.currentText())
        algorithm: str = self.algorithm_combo.currentText()

        # Define valid key sizes for each algorithm
        valid_key_sizes = {
            "3DES": [64, 128, 192],
            "Camellia": [128, 192, 256],
            "Blowfish": [32, 64, 128, 192, 256, 448],
            "ChaCha20": [256],
        }

        # Check if the selected key size is valid for the chosen algorithm
        if sym_key_size not in valid_key_sizes.get(algorithm, []):
            QMessageBox.critical(self, "Ошибка", f"Неправильный размер ключа для алгоритма {algorithm}.")
            return

        symmetric_key_path: str = self.save_file_path("Укажите путь для сохранения симметричного ключа (symmetric)")
        public_key_path: str = self.save_file_path("Укажите путь для сохранения публичного ключа (public)")
        private_key_path: str = self.save_file_path("Укажите путь для сохранения приватного ключа (private)")

        self.cryptography = CryptographySystem(
            symmetric_key_path, public_key_path, private_key_path, rsa_key_size,
            sym_key_size, algorithm
        )
        try:
            self.cryptography.key_generation()
            QMessageBox.information(self, "Success", "Ключи успешно сгенерированы и сохранены.")
        except Exception as ex:
            logging.error(f"Ошибка при генерации ключей: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при генерации ключей: {ex}")

    def encrypt_text(self) -> None:
        """
        Encrypt the text file using the generated keys.
        """
        if not self.cryptography:
            QMessageBox.warning(self, "Warning", "Сначала сгенерируйте ключи!")
            return

        base_text_path: str = self.get_file_path("Укажите путь к файлу с исходным текстом")
        encrypted_text_path: str = self.save_file_path("Укажите путь для сохранения зашифрованного текста")

        try:
            self.cryptography.encrypt_file(base_text_path, encrypted_text_path)
            QMessageBox.information(self, "Success", "Текст успешно зашифрован.")
        except Exception as ex:
            logging.error(f"Ошибка при шифрованиании текста: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при шифровании текста: {ex}")

    def decrypt_text(self) -> None:
        """
        Decrypt the text file using the generated keys.
        """
        if not self.cryptography:
            QMessageBox.warning(self, "Warning", "Сначала сгенерируйте ключи!")
            return

        encrypted_text_path: str = self.get_file_path("Укажите путь к файлу с зашифрованным текстом")
        decrypted_text_path: str = self.save_file_path("Укажите путь для сохранения расшифрованного текста")

        try:
            self.cryptography.decrypt_file(encrypted_text_path, decrypted_text_path)
            QMessageBox.information(self, "Success", "Текст успешно расшифрован.")
        except Exception as ex:
            logging.error(f"Ошибка при расшифровании текста: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при расшифровании текста: {ex}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())
