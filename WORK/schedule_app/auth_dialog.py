import logging
import re

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from register_dialog import RegisterDialog
from db import SessionLocal
from models import User
import bcrypt

logger = logging.getLogger(__name__)


class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.resize(300, 160)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Имя пользователя:"))
        self.edit_login = QLineEdit()
        layout.addWidget(self.edit_login)

        layout.addWidget(QLabel("Пароль:"))
        self.edit_pass = QLineEdit()
        self.edit_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass)

        self.btn_login = QPushButton("Войти")
        self.btn_reg = QPushButton("Регистрация")
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_reg)

        self.btn_login.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.open_register)

        self.user = None

    def login(self):
        username = self.edit_login.text().strip()
        password = self.edit_pass.text()

        logger.info("Попытка входа пользователя '%s'", username)

        # Краткие проверки на месте
        if not username or not password:
            logger.warning("Пустой логин или пароль")
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        # Логин разрешён: только буквы, цифры, подчёркивания, длина 3–30
        if not re.match(r'^[A-Za-z0-9_]{3,30}$', username):
            logger.warning("Неверный формат логина: '%s'", username)
            QMessageBox.warning(self, "Ошибка", "Неверный формат логина")
            return

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(username=username).first()
            if user is None:
                logger.warning("Пользователь '%s' не найден", username)
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                logger.info("Пользователь '%s' успешно вошёл", username)
                self.user = user
                self.accept()
            else:
                logger.warning("Неверный пароль для пользователя '%s'", username)
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
        except Exception as e:
            logger.exception("Ошибка при запросе к БД в методе login")
            QMessageBox.critical(self, "Ошибка", "Внутренняя ошибка входа. Подробности в логах.")
        finally:
            db.close()
            SessionLocal.remove()

    def open_register(self):
        logger.info("Открытие окна регистрации")
        dlg = RegisterDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            logger.info("Регистрация прошла успешно, возвращаемся к окну входа")
            QMessageBox.information(self, "Успех", "Регистрация завершена. Войдите в систему.")
        else:
            logger.info("Пользователь отменил регистрацию")
