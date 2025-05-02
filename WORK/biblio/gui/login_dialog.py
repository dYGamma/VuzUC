from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
import controllers

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему библиотеки")

        self.user_id = QLineEdit()
        self.user_id.setPlaceholderText("ID ученика / библиотекаря")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Пароль")

        btn = QPushButton("Войти")
        btn.clicked.connect(self.attempt_login)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ID:"));     layout.addWidget(self.user_id)
        layout.addWidget(QLabel("Пароль:")); layout.addWidget(self.password)
        layout.addWidget(btn)

        self.user = None

    def attempt_login(self):
        uid = self.user_id.text().strip()
        pw  = self.password.text().strip()
        role = controllers.authenticate(uid, pw)
        if role:
            self.user = controllers.get_user(uid)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
