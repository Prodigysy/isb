import sys
import logging
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QComboBox,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout
)

from crypto_system import Cryptography  

logging.basicConfig(level=logging.INFO)

class CryptoApp(QMainWindow):
    def __init__(self):
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
        sym_key_size_layout.addWidget(self.sym_key_size_label)
        sym_key_size_layout.addWidget(self.sym_key_size_combo)
        layout.addLayout(sym_key_size_layout)

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

        self.cryptography = None

    def get_file_path(self, prompt):
        file_path, _ = QFileDialog.getOpenFileName(self, prompt, "", "All Files (*)")
        return file_path

    def save_file_path(self, prompt):
        file_path, _ = QFileDialog.getSaveFileName(self, prompt, "", "All Files (*)")
        return file_path

    def generate_keys(self):
        symmetric_key_path = self.save_file_path("Укажите путь для сохранения симметричного ключа (symmetric)")
        public_key_path = self.save_file_path("Укажите путь для сохранения публичного ключа (public)")
        private_key_path = self.save_file_path("Укажите путь для сохранения приватного ключа (private)")
        rsa_key_size = int(self.key_size_combo.currentText())
        sym_key_size_bits = int(self.sym_key_size_combo.currentText())

        self.cryptography = Cryptography(symmetric_key_path, public_key_path, private_key_path, rsa_key_size, sym_key_size_bits)
        try:
            self.cryptography.key_generation()
            QMessageBox.information(self, "Success", "Ключи успешно сгенерированы и сохранены.")
        except Exception as ex:
            logging.error(f"Ошибка при генерации ключей: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при генерации ключей: {ex}")

    def encrypt_text(self):
        if not self.cryptography:
            QMessageBox.warning(self, "Warning", "Сначала сгенерируйте ключи!")
            return

        base_text_path = self.get_file_path("Укажите путь к файлу с исходным текстом")
        encrypted_text_path = self.save_file_path("Укажите путь для сохранения зашифрованного текста")

        try:
            self.cryptography.encryption(base_text_path, encrypted_text_path)
            QMessageBox.information(self, "Success", "Текст успешно зашифрован.")
        except Exception as ex:
            logging.error(f"Ошибка при шифровании текста: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при шифровании текста: {ex}")

    def decrypt_text(self):
        if not self.cryptography:
            QMessageBox.warning(self, "Warning", "Сначала сгенерируйте ключи!")
            return

        encrypted_text_path = self.get_file_path("Укажите путь к файлу с зашифрованным текстом")
        decrypted_text_path = self.save_file_path("Укажите путь для сохранения расшифрованного текста")

        try:
            self.cryptography.decryption(encrypted_text_path, decrypted_text_path)
            QMessageBox.information(self, "Success", "Текст успешно расшифрован.")
        except Exception as ex:
            logging.error(f"Ошибка при расшифровании текста: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при расшифровании текста: {ex}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())
