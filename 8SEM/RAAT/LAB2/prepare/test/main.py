import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont

class CustomMessageBox(QDialog):
    """
    Кастомное диалоговое окно для отображения сообщений.
    """
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9;")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        # Текст сообщения
        self.message_label = QLabel(message)
        self.message_label.setFont(QFont("Arial", 12))
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        # Кнопка "OK"
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet(
            "background-color: #5E81AC; color: #D8DEE9; border: none; padding: 10px; font-size: 14px;"
        )
        self.ok_button.clicked.connect(self.close)
        layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)


class InputValidator:
    """
    Класс для проверки корректности ввода данных.
    """
    def validate_number(self, input_str):
        try:
            float(input_str)
            return True
        except ValueError:
            return False

    def is_zero(self, divisor):
        return divisor == 0


class ErrorLogger:
    """
    Класс для логирования ошибок.
    """
    def __init__(self, parent):
        self.parent = parent

    def log_error(self, msg):
        dialog = CustomMessageBox("Ошибка", msg, self.parent)
        dialog.exec_()


class Calculator:
    """
    Класс для выполнения операции деления.
    """
    def __init__(self, parent):
        self.validator = InputValidator()
        self.logger = ErrorLogger(parent)

    def divide(self, dividend_str, divisor_str):
        if not self.validator.validate_number(dividend_str) or not self.validator.validate_number(divisor_str):
            self.logger.log_error("Ошибка ввода данных")
            return None
        dividend = float(dividend_str)
        divisor = float(divisor_str)
        if self.validator.is_zero(divisor):
            self.logger.log_error("Деление на ноль невозможно")
            return None
        return dividend / divisor


class FileManager:
    """
    Класс для работы с файлами (сохранение и загрузка истории операций).
    """
    def __init__(self, file_path="history.txt"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()

    def save_result(self, result):
        with open(self.file_path, 'a') as file:
            file.write(f"{result}\n")

    def load_history(self):
        with open(self.file_path, 'r') as file:
            return file.readlines()


class MainWindow(QMainWindow):
    """
    Основное окно приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9;")

        # Инициализация классов
        self.calculator = Calculator(self)
        self.file_manager = FileManager()

        # Создание интерфейса
        self.init_ui()

    def init_ui(self):
        # Основной контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Заголовок
        title = QLabel("Калькулятор деления")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поля ввода
        input_layout = QVBoxLayout()
        self.dividend_input = QLineEdit()
        self.dividend_input.setPlaceholderText("Введите делимое")
        self.dividend_input.setStyleSheet("background-color: #4C566A; color: #D8DEE9; border: none; padding: 10px;")
        input_layout.addWidget(self.dividend_input)

        self.divisor_input = QLineEdit()
        self.divisor_input.setPlaceholderText("Введите делитель")
        self.divisor_input.setStyleSheet("background-color: #4C566A; color: #D8DEE9; border: none; padding: 10px;")
        input_layout.addWidget(self.divisor_input)

        layout.addLayout(input_layout)

        # Кнопка "Calculate"
        self.calculate_btn = QPushButton("Вычислить")
        self.calculate_btn.setStyleSheet(
            "background-color: #5E81AC; color: #D8DEE9; border: none; padding: 10px; font-size: 14px;"
        )
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)

        # Кнопка "Show History"
        self.history_btn = QPushButton("История вычислений")
        self.history_btn.setStyleSheet(
            "background-color: #81A1C1; color: #D8DEE9; border: none; padding: 10px; font-size: 14px;"
        )
        self.history_btn.clicked.connect(self.show_history)
        layout.addWidget(self.history_btn)

        # # Анимация кнопок
        # self.animate_buttons()

    def animate_buttons(self):
        # Анимация для кнопки "Calculate"
        self.anim_calculate = QPropertyAnimation(self.calculate_btn, b"geometry")
        self.anim_calculate.setDuration(1000)
        self.anim_calculate.setStartValue(self.calculate_btn.geometry())
        self.anim_calculate.setEndValue(QRect(
            self.calculate_btn.x(), self.calculate_btn.y() - 10,
            self.calculate_btn.width(), self.calculate_btn.height()
        ))
        self.anim_calculate.setEasingCurve(QEasingCurve.OutBounce)
        self.anim_calculate.start()

        # Анимация для кнопки "Show History"
        self.anim_history = QPropertyAnimation(self.history_btn, b"geometry")
        self.anim_history.setDuration(1000)
        self.anim_history.setStartValue(self.history_btn.geometry())
        self.anim_history.setEndValue(QRect(
            self.history_btn.x(), self.history_btn.y() + 10,
            self.history_btn.width(), self.history_btn.height()
        ))
        self.anim_history.setEasingCurve(QEasingCurve.OutBounce)
        self.anim_history.start()

    def calculate(self):
        dividend = self.dividend_input.text()
        divisor = self.divisor_input.text()
        result = self.calculator.divide(dividend, divisor)
        if result is not None:
            self.file_manager.save_result(result)
            dialog = CustomMessageBox("Результат", f"Результат: {result}", self)
            dialog.exec_()

    def show_history(self):
        history = self.file_manager.load_history()
        if history:
            history_str = "\n".join([line.strip() for line in history])
            dialog = CustomMessageBox("История", history_str, self)
            dialog.exec_()
        else:
            dialog = CustomMessageBox("История", "История операций пуста", self)
            dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())