import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,QTableWidget,
    QTableWidgetItem,QFormLayout,QComboBox,QGroupBox,QFileDialog,QMessageBox,QSplitter,
    QHeaderView,QSizePolicy
)

import sqlite3
import pandas as pd


class UserManagementWindow(QWidget):
    def closeEvent(self,event):
        """Закрываем соединение с БД при закрытии окна"""
        self.conn.close()
        event.accept()

    def import_users(self):
        options = QFileDialog.Options()
        file_name,_ = QFileDialog.getOpenFileName(self,"Import Users","","Excel Files (*.xls *.xlsx)",options=options)
        if file_name:
            try:
                users_df = pd.read_excel(file_name)
            except Exception as e:
                QMessageBox.critical(self,"Ошибка",f"Ошибка при импорте пользователей: {str(e)}")
                return

            if users_df.empty:
                QMessageBox.warning(self,"Внимание","Файл с пользователями пуст.")
                return

            users_data = users_df.values.tolist()
            for user_data in users_data:
                if len(user_data) == 4:
                    full_name,username,password,permissions = user_data
                    # Проверка на существующего пользователя
                    self.cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
                    if self.cursor.fetchone() is None:
                        self.cursor.execute(
                            "INSERT INTO users (full_name, username, password, permissions) VALUES (?, ?, ?, ?)",
                            (full_name,username,password,permissions))
            self.conn.commit()
            self.load_user_data()

    def export_users(self):
        options = QFileDialog.Options()
        file_name,_ = QFileDialog.getSaveFileName(self,"Export Users","","Excel Files (*.xlsx)",options=options)
        if file_name:
            query = "SELECT full_name, username, password, permissions FROM users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            users_df = pd.DataFrame(users,columns=["Full Name","Username","Password","Permissions"])
            users_df.to_excel(file_name,index=False)

    def __init__(self,previous_window,login_window,username):
        super().__init__()
        self.previous_window = previous_window
        self.login_window = login_window
        self.username = username
        self.init_db()
        self.init_ui()
        self.load_user_data()
        self.setWindowTitle("Управление пользователями")
        self.showMaximized()

    def init_db(self):
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                full_name
                                TEXT
                                NOT
                                NULL,
                                username
                                TEXT
                                NOT
                                NULL
                                UNIQUE,
                                password
                                TEXT
                                NOT
                                NULL,
                                permissions
                                TEXT
                                NOT
                                NULL
                            )
                            ''')
        self.conn.commit()

    # def init_ui(self):
    #     main_layout = QVBoxLayout(self)
    #     main_layout.setContentsMargins(10,10,10,10)
    #     main_layout.setSpacing(10)
    #
    #     # Top bar
    #     top_bar = QHBoxLayout()
    #     self.back_button = QPushButton("← Назад")
    #     self.logout_button = QPushButton("Выход")
    #     self.user_label = QLabel(f"Пользователь: {self.username}")
    #
    #     top_bar.addWidget(self.back_button)
    #     top_bar.addStretch()
    #     top_bar.addWidget(self.user_label)
    #     top_bar.addWidget(self.logout_button)
    #
    #     # Main content
    #     splitter = QSplitter(Qt.Horizontal)
    #
    #     # Left panel - Table
    #     left_widget = QWidget()
    #     left_layout = QVBoxLayout(left_widget)
    #     left_layout.setContentsMargins(0,0,0,0)
    #
    #     self.user_table = QTableWidget()
    #     self.user_table.setColumnCount(5)
    #     self.user_table.setHorizontalHeaderLabels(["ID","Полное имя","Логин","Пароль","Права"])
    #     self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     self.user_table.verticalHeader().setVisible(False)
    #     self.user_table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    #
    #     left_layout.addWidget(self.user_table)
    #
    #     # Right panel - Forms
    #     right_widget = QWidget()
    #     right_layout = QVBoxLayout(right_widget)
    #     right_layout.setContentsMargins(10,0,0,0)
    #     right_layout.setSpacing(10)
    #
    #     # Add user form
    #     add_group = QGroupBox("Добавление пользователя")
    #     add_layout = QFormLayout()
    #     self.full_name_input = QLineEdit()
    #     self.username_input = QLineEdit()
    #     self.password_input = QLineEdit()
    #     self.permissions_combo = QComboBox()
    #     self.permissions_combo.addItems(["Полный доступ","Средний доступ","Ограниченный доступ"])
    #     add_button = QPushButton("Добавить")
    #
    #     add_layout.addRow("Полное имя:",self.full_name_input)
    #     add_layout.addRow("Логин:",self.username_input)
    #     add_layout.addRow("Пароль:",self.password_input)
    #     add_layout.addRow("Права:",self.permissions_combo)
    #     add_layout.addRow(add_button)
    #     add_group.setLayout(add_layout)
    #
    #     # Edit user form
    #     edit_group = QGroupBox("Редактирование пользователя")
    #     edit_layout = QFormLayout()
    #     self.edit_id_input = QLineEdit()
    #     self.edit_full_name_input = QLineEdit()
    #     self.edit_username_input = QLineEdit()
    #     self.edit_password_input = QLineEdit()
    #     self.edit_permissions_combo = QComboBox()
    #     self.edit_permissions_combo.addItems(["Полный доступ","Средний доступ","Ограниченный доступ"])
    #     save_edit_button = QPushButton("Сохранить")
    #
    #     edit_layout.addRow("ID:",self.edit_id_input)
    #     edit_layout.addRow("Полное имя:",self.edit_full_name_input)
    #     edit_layout.addRow("Логин:",self.edit_username_input)
    #     edit_layout.addRow("Пароль:",self.edit_password_input)
    #     edit_layout.addRow("Права:",self.edit_permissions_combo)
    #     edit_layout.addRow(save_edit_button)
    #     edit_group.setLayout(edit_layout)
    #
    #     # Search/Delete
    #     manage_group = QGroupBox("Управление")
    #     manage_layout = QFormLayout()
    #     self.search_input = QLineEdit()
    #     search_button = QPushButton("Найти")
    #     delete_button = QPushButton("Удалить")
    #     import_button = QPushButton("Импорт")
    #     export_button = QPushButton("Экспорт")
    #
    #     manage_layout.addRow("Поиск (ID):",self.search_input)
    #     manage_layout.addRow(search_button)
    #     manage_layout.addRow(delete_button)
    #     manage_layout.addRow(import_button)
    #     manage_layout.addRow(export_button)
    #     manage_group.setLayout(manage_layout)
    #
    #     right_layout.addWidget(add_group)
    #     right_layout.addWidget(edit_group)
    #     right_layout.addWidget(manage_group)
    #     right_layout.addStretch()
    #
    #     splitter.addWidget(left_widget)
    #     splitter.addWidget(right_widget)
    #     splitter.setSizes([self.width() * 2 // 3,self.width() // 3])
    #
    #     main_layout.addLayout(top_bar)
    #     main_layout.addWidget(splitter)
    #
    #     # Connections
    #     self.back_button.clicked.connect(self.back_function)
    #     self.logout_button.clicked.connect(self.logout)
    #     add_button.clicked.connect(self.add_user)
    #     save_edit_button.clicked.connect(self.save_edit_user)
    #     search_button.clicked.connect(self.search_user)
    #     delete_button.clicked.connect(self.delete_user)
    #     import_button.clicked.connect(self.import_users)
    #     export_button.clicked.connect(self.export_users)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)

        # Top bar
        top_bar = QHBoxLayout()
        self.back_button = QPushButton("← Назад")
        self.logout_button = QPushButton("Выход")
        self.user_label = QLabel(f"Пользователь: {self.username}")

        top_bar.addWidget(self.back_button)
        top_bar.addStretch()
        top_bar.addWidget(self.user_label)
        top_bar.addWidget(self.logout_button)

        # Main content
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - Table
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0,0,0,0)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID","Полное имя","Логин","Пароль","Права"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        left_layout.addWidget(self.user_table)

        # Right panel - Forms
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10,0,0,0)
        right_layout.setSpacing(10)

        # Информационная плашка
        info_box = QGroupBox("Справка")

        info_text = QLabel(
            "Этот раздел предоставляет возможность просматривать, добавлять, редактировать и удалять информацию о пользователях.\n\n"
            "▪ Для просмотра данных используйте таблицу слева\n"
            "▪ Для добавления нового пользователя заполните поля ниже\n"
            "▪ Для редактирования введите ID и внесите изменения\n"
            "▪ Для удаления введите ID пользователя(ей)\n"
            "▪ Используйте кнопки Импорт/Экспорт для работы с Excel"
        )
        info_text.setWordWrap(True)

        info_layout = QVBoxLayout(info_box)
        info_layout.addWidget(info_text)

        # Добавляем информационную плашку в начало правой панели
        right_layout.addWidget(info_box)

        # Add user form
        add_group = QGroupBox("Добавление пользователя")
        add_layout = QFormLayout()
        self.full_name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.permissions_combo = QComboBox()
        self.permissions_combo.addItems(["Полный доступ","Средний доступ","Ограниченный доступ"])
        add_button = QPushButton("Добавить")

        add_layout.addRow("Полное имя:",self.full_name_input)
        add_layout.addRow("Логин:",self.username_input)
        add_layout.addRow("Пароль:",self.password_input)
        add_layout.addRow("Права:",self.permissions_combo)
        add_layout.addRow(add_button)
        add_group.setLayout(add_layout)

        # Edit user form
        edit_group = QGroupBox("Редактирование пользователя")
        edit_layout = QFormLayout()
        self.edit_id_input = QLineEdit()
        self.edit_full_name_input = QLineEdit()
        self.edit_username_input = QLineEdit()
        self.edit_password_input = QLineEdit()
        self.edit_permissions_combo = QComboBox()
        self.edit_permissions_combo.addItems(["Полный доступ","Средний доступ","Ограниченный доступ"])
        save_edit_button = QPushButton("Сохранить")

        edit_layout.addRow("ID:",self.edit_id_input)
        edit_layout.addRow("Полное имя:",self.edit_full_name_input)
        edit_layout.addRow("Логин:",self.edit_username_input)
        edit_layout.addRow("Пароль:",self.edit_password_input)
        edit_layout.addRow("Права:",self.edit_permissions_combo)
        edit_layout.addRow(save_edit_button)
        edit_group.setLayout(edit_layout)

        # Search/Delete
        manage_group = QGroupBox("Управление")
        manage_layout = QFormLayout()
        self.search_input = QLineEdit()
        search_button = QPushButton("Найти")
        delete_button = QPushButton("Удалить")
        import_button = QPushButton("Импорт")
        export_button = QPushButton("Экспорт")

        manage_layout.addRow("Поиск (ID):",self.search_input)
        manage_layout.addRow(search_button)
        manage_layout.addRow(delete_button)
        manage_layout.addRow(import_button)
        manage_layout.addRow(export_button)
        manage_group.setLayout(manage_layout)

        right_layout.addWidget(add_group)
        right_layout.addWidget(edit_group)
        right_layout.addWidget(manage_group)
        right_layout.addStretch()

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([self.width() * 2 // 3,self.width() // 3])

        main_layout.addLayout(top_bar)
        main_layout.addWidget(splitter)

        # Connections
        self.back_button.clicked.connect(self.back_function)
        self.logout_button.clicked.connect(self.logout)
        add_button.clicked.connect(self.add_user)
        save_edit_button.clicked.connect(self.save_edit_user)
        search_button.clicked.connect(self.search_user)
        delete_button.clicked.connect(self.delete_user)
        import_button.clicked.connect(self.import_users)
        export_button.clicked.connect(self.export_users)

    def logout(self):
        self.login_window.show()
        self.close()

    def back_function(self):
        self.previous_window.show()
        self.close()

    def load_user_data(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()

        self.user_table.setRowCount(len(users))
        for row_idx,user in enumerate(users):
            for col_idx,data in enumerate(user):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEnabled)
                self.user_table.setItem(row_idx,col_idx,item)

    def add_user(self):
        full_name = self.full_name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        permissions = self.permissions_combo.currentText()

        if not all([full_name,username,password]):
            QMessageBox.warning(self,"Ошибка","Все поля должны быть заполнены!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO users (full_name, username, password, permissions) VALUES (?, ?, ?, ?)",
                (full_name,username,password,permissions)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self,"Ошибка","Пользователь с таким логином уже существует!")
            return

        self.full_name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.load_user_data()

    def search_user(self):
        user_id = self.search_input.text().strip()
        if not user_id:
            self.load_user_data()
            return

        try:
            user_id = int(user_id)
        except ValueError:
            QMessageBox.warning(self,"Ошибка","ID должен быть числом!")
            return

        self.cursor.execute("SELECT * FROM users WHERE id = ?",(user_id,))
        user = self.cursor.fetchone()
        if user:
            self.user_table.setRowCount(1)
            for col_idx,data in enumerate(user):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEnabled)
                self.user_table.setItem(0,col_idx,item)
        else:
            QMessageBox.information(self,"Информация","Пользователь не найден")

    def delete_user(self):
        user_id = self.search_input.text().strip()
        if not user_id:
            QMessageBox.warning(self,"Ошибка","Введите ID пользователя!")
            return

        try:
            user_id = int(user_id)
        except ValueError:
            QMessageBox.warning(self,"Ошибка","ID должен быть числом!")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить пользователя с ID {user_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM users WHERE id = ?",(user_id,))
            self.conn.commit()
            self.load_user_data()

    def save_edit_user(self):
        user_id = self.edit_id_input.text().strip()
        full_name = self.edit_full_name_input.text().strip()
        username = self.edit_username_input.text().strip()
        password = self.edit_password_input.text().strip()
        permissions = self.edit_permissions_combo.currentText()

        if not all([user_id,full_name,username,password]):
            QMessageBox.warning(self,"Ошибка","Все поля должны быть заполнены!")
            return

        try:
            self.cursor.execute(
                """UPDATE users
                   SET full_name   = ?,
                       username    = ?,
                       password    = ?,
                       permissions = ?
                   WHERE id = ?""",
                (full_name,username,password,permissions,user_id)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self,"Ошибка","Пользователь с таким логином уже существует!")
            return

        self.edit_id_input.clear()
        self.edit_full_name_input.clear()
        self.edit_username_input.clear()
        self.edit_password_input.clear()
        self.load_user_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserManagementWindow(None,None,"admin")
    window.show()
    sys.exit(app.exec_())