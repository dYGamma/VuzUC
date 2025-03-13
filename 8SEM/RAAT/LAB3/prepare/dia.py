import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class InputValidator:
    """
    Класс для проверки корректности вводимых данных.
    """
    def validate_number(self, input_str):
        try:
            n = int(input_str)
            return n >= 0  # только неотрицательные числа
        except ValueError:
            return False

class FibonacciCalculator:
    """
    Класс для вычисления чисел Фибоначчи.
    Используется итеративный метод для обеспечения оптимальности.
    """
    def calculate(self, n: int):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def calculate_sequence(self, n: int):
        """
        Метод для вычисления последовательности Фибоначчи до n-го элемента.
        """
        sequence = []
        if n <= 0:
            return sequence
        a, b = 0, 1
        sequence.append(a)
        if n == 1:
            return sequence
        sequence.append(b)
        for _ in range(2, n):
            a, b = b, a + b
            sequence.append(b)
        return sequence

class ErrorLogger:
    """
    Класс для отображения сообщений об ошибках.
    """
    def show_error(self, message, parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()

class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор чисел Фибоначчи")
        self.setFixedSize(500, 300)
        self.calculator = FibonacciCalculator()
        self.validator = InputValidator()
        self.error_logger = ErrorLogger()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный контейнер
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        central_widget.setLayout(layout)
        
        # Заголовок
        title = QLabel("Калькулятор чисел Фибоначчи")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Контейнер для ввода
        input_layout = QHBoxLayout()
        input_label = QLabel("Введите номер элемента:")
        input_label.setFont(QFont("Arial", 14))
        input_layout.addWidget(input_label)
        
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 14))
        self.input_field.setPlaceholderText("Например, 10")
        input_layout.addWidget(self.input_field)
        layout.addLayout(input_layout)
        
        # Кнопка для расчёта
        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.setFont(QFont("Arial", 14))
        self.calc_button.clicked.connect(self.calculate_fibonacci)
        layout.addWidget(self.calc_button)
        
        # Метка для вывода результата
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Применяем стили для красивого оформления
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QLabel {
                color: #D8DEE9;
            }
            QLineEdit {
                background-color: #4C566A;
                color: #D8DEE9;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #D8DEE9;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)

    def calculate_fibonacci(self):
        input_text = self.input_field.text().strip()
        if not self.validator.validate_number(input_text):
            self.error_logger.show_error("Пожалуйста, введите целое неотрицательное число.", self)
            return
        n = int(input_text)
        result = self.calculator.calculate(n)
        self.result_label.setText(f"F({n}) = {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
