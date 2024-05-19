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

import crypto as cp

logging.basicConfig(level=logging.INFO)

class CryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Система шифрования с помощью TripleDes")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.sym_key_label = QLabel("Путь для сохранения симметричного ключа (symmetric):")
        self.sym_key_edit = QLineEdit()
        layout.addWidget(self.sym_key_label)
        layout.addWidget(self.sym_key_edit)

        self.pub_key_label = QLabel("Путь для сохранения публичного ключа (public):")
        self.pub_key_edit = QLineEdit()
        layout.addWidget(self.pub_key_label)
        layout.addWidget(self.pub_key_edit)

        self.priv_key_label = QLabel("Путь для сохранения приватного ключа (private):")
        self.priv_key_edit = QLineEdit()
        layout.addWidget(self.priv_key_label)
        layout.addWidget(self.priv_key_edit)

        key_size_layout = QHBoxLayout()
        self.key_size_label = QLabel("Выберите размер ключа:")
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItem("8")
        self.key_size_combo.addItem("16")
        self.key_size_combo.addItem("24")
        key_size_layout.addWidget(self.key_size_label)
        key_size_layout.addWidget(self.key_size_combo)
        layout.addLayout(key_size_layout)

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
        """Prompt the user to enter a file path."""
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ShowDirsOnly
        file_path, _ = QFileDialog.getOpenFileName(self, prompt, "", options=options)
        return file_path

    def generate_keys(self):
        symmetric_key_path = self.sym_key_edit.text()
        public_key_path = self.pub_key_edit.text()
        private_key_path = self.priv_key_edit.text()
        key_size = int(self.key_size_combo.currentText())

        self.cryptography = cp.Cryptography(symmetric_key_path, public_key_path, private_key_path, key_size)
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
        encrypted_text_path, _ = QFileDialog.getSaveFileName(self, "Укажите путь для сохранения зашифрованного текста", "", "All Files (*)")

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
        decrypted_text_path, _ = QFileDialog.getSaveFileName(self, "Укажите путь для сохранения расшифрованного текста", "", "All Files (*)")

        try:
            self.cryptography.decryption(encrypted_text_path, decrypted_text_path)
            QMessageBox.information(self, "Success", "Текст успешно расшифрован.")
        except Exception as ex:
            logging.error(f"Ошибка при расшифровании текста: {ex}")
            QMessageBox.critical(self, "Error", f"Ошибка при расшифровании текста: {ex}")


def main():
    app = QApplication(sys.argv)
    crypto_app = CryptoApp()
    crypto_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
