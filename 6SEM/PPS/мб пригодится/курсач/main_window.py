import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QDesktopWidget
from PyQt5.QtCore import Qt

import sqlite3

class MainMenuWindow(QWidget):
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Main Menu")
        self.setFullScreen()

        self.username = username
        self.init_db()
        self.init_ui()

    def setFullScreen(self):
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
        self.setGeometry(screen_geometry)

    def init_db(self):
        # Connect to SQLite database (create a new one if it doesn't exist)
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()

        # Create a table to store sales information if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                saler_name TEXT NOT NULL,
                region TEXT NOT NULL,
                date TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        # Top GroupBox with buttons and labels
        top_layout = QHBoxLayout()
        home_button = QPushButton("Домой")
        window_name_label = QLabel("Главное меню системы")
        username_label = QLabel(f"Username: {self.username}")

        top_layout.addWidget(home_button)
        top_layout.addWidget(window_name_label)
        top_layout.addWidget(username_label)

        top_groupbox = QGroupBox()
        top_groupbox.setLayout(top_layout)

        # Left GroupBox: Table from DB (including sales information)
        left_layout = QVBoxLayout()
        table_label = QLabel("Таблица из базы данных (Продажи):")
        sales_table = QTableWidget()
        sales_table.setColumnCount(6)
        sales_table.setHorizontalHeaderLabels(["ID", "Product Name", "Saler Name", "Region", "Date", "Price"])

        # Fetch and display sales information
        query = "SELECT * FROM sales"
        self.cursor.execute(query)
        sales_data = self.cursor.fetchall()

        sales_table.setRowCount(len(sales_data))
        for row, sale in enumerate(sales_data):
            for col, value in enumerate(sale):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)  # Make cells read-only
                sales_table.setItem(row, col, item)

        left_layout.addWidget(table_label)
        left_layout.addWidget(sales_table)

        left_groupbox = QGroupBox()
        left_groupbox.setLayout(left_layout)

        # Center GroupBox: Buttons (as before)
        center_layout = QVBoxLayout()
        button_home = QPushButton("Домой")
        button_sales = QPushButton("Управление продажами")
        button_analysis = QPushButton("Анализ продаж")
        button_reports = QPushButton("Отчеты")
        button_trends = QPushButton("Тренды и паттерны")

        center_layout.addWidget(button_home)
        center_layout.addWidget(button_sales)
        center_layout.addWidget(button_analysis)
        center_layout.addWidget(button_reports)
        center_layout.addWidget(button_trends)

        center_groupbox = QGroupBox()
        center_groupbox.setLayout(center_layout)

        # Right GroupBox: Label with long text (as before)
        right_layout = QVBoxLayout()
        long_text_label = QLabel(
            "Это длинный текст, который может содержать информацию, требующую внимания пользователя. "
            "Здесь могут быть различные уведомления или инструкции для пользователя."
        )
        long_text_label.setWordWrap(True)

        right_layout.addWidget(long_text_label)

        right_groupbox = QGroupBox()
        right_groupbox.setLayout(right_layout)

        # Main Layout: Horizontal arrangement of left, center, and right GroupBoxes
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_groupbox, 6)  # 60%
        main_layout.addWidget(center_groupbox, 2)  # 20%
        main_layout.addWidget(right_groupbox, 2)  # 20%

        # Overall Layout: Vertical arrangement of top and main layouts
        overall_layout = QVBoxLayout()
        overall_layout.addWidget(top_groupbox)
        overall_layout.addLayout(main_layout)

        self.setLayout(overall_layout)

                # Signals and slots for buttons (placeholder functions)
        button_home.clicked.connect(self.go_home)
        button_sales.clicked.connect(self.manage_sales)
        button_analysis.clicked.connect(self.analyze_sales)
        button_reports.clicked.connect(self.generate_reports)
        button_trends.clicked.connect(self.analyze_trends)

    # Placeholder functions for button actions
    def go_home(self):
        pass  # Replace with actual logic

    def manage_sales(self):
        pass  # Replace with actual logic

    def analyze_sales(self):
        pass  # Replace with actual logic

    def generate_reports(self):
        pass  # Replace with actual logic

    def analyze_trends(self):
        pass  # Replace with actual logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "YourUsername"  # Replace with the actual username
    main_menu_window = MainMenuWindow(username)
    main_menu_window.show()
    sys.exit(app.exec_())
