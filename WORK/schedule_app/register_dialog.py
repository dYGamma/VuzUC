import logging
import re

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
import bcrypt
from db import SessionLocal
from models import User, RoleEnum

logger = logging.getLogger(__name__)


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.resize(350, 240)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Имя пользователя (3–30 символов):"))
        self.edit_login = QLineEdit()
        layout.addWidget(self.edit_login)

        layout.addWidget(QLabel("Пароль:"))
        self.edit_pass = QLineEdit()
        self.edit_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass)

        layout.addWidget(QLabel("Подтвердите пароль:"))
        self.edit_pass2 = QLineEdit()
        self.edit_pass2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass2)

        layout.addWidget(QLabel("Роль:"))
        self.combo_role = QComboBox()
        # Разрешаем выбор только student и parent; admin — вручную через БД
        self.combo_role.addItems([RoleEnum.student.value, RoleEnum.parent.value])
        layout.addWidget(self.combo_role)

        self.btn_ok = QPushButton("Зарегистрироваться")
        self.btn_cancel = QPushButton("Отмена")
        layout.addWidget(self.btn_ok)
        layout.addWidget(self.btn_cancel)

        self.btn_ok.clicked.connect(self.register)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_username(self, username: str) -> bool:
        """Допустимые символы: буквы, цифры, _, длина 3–30"""
        return bool(re.match(r'^[A-Za-z0-9_]{3,30}$', username))

    def validate_password(self, pw: str) -> bool:
        """
        Пароль не менее 8 символов, содержит:
        - заглавную букву
        - строчную букву
        - цифру
        - спецсимвол (любой не-алфавитно-цифровой, включая _)
        """
        if len(pw) < 8:
            return False
        if not re.search(r"[A-Z]", pw):
            return False
        if not re.search(r"[a-z]", pw):
            return False
        if not re.search(r"\d", pw):
            return False
        # Любой символ, который НЕ буква и НЕ цифра
        if not re.search(r"[^A-Za-z0-9]", pw):
            return False
        return True

    def register(self):
        username = self.edit_login.text().strip()
        pw1 = self.edit_pass.text()
        pw2 = self.edit_pass2.text()
        role = self.combo_role.currentText()

        logger.info("Попытка регистрации пользователя '%s' с ролью '%s'", username, role)

        # Проверки на форме
        if not username:
            logger.warning("Пустой логин при регистрации")
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя")
            return
        if not self.validate_username(username):
            logger.warning("Неверный формат логина при регистрации: '%s'", username)
            QMessageBox.warning(
                self, "Ошибка",
                "Логин должен быть 3–30 символов: буквы, цифры или _"
            )
            return

        if pw1 != pw2:
            logger.warning("Пароли не совпадают при регистрации '%s'", username)
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        if not self.validate_password(pw1):
            logger.warning("Слабый пароль при регистрации '%s'", username)
            QMessageBox.warning(
                self, "Ошибка",
                "Пароль должен быть ≥8 символов и содержать:\n"
                "Заглавную, строчную букву, цифру и спецсимвол (например, _ или !@#)"
            )
            return

        db = SessionLocal()
        try:
            # Проверка существующего пользователя
            if db.query(User).filter_by(username=username).first():
                logger.warning("Пользователь '%s' уже существует", username)
                QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
                return

            # Хешируем и сохраняем
            pw_hash = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt()).decode()
            user = User(username=username, password_hash=pw_hash, role=RoleEnum(role))
            db.add(user)
            try:
                db.commit()
                logger.info("Пользователь '%s' успешно зарегистрирован", username)
            except Exception:
                db.rollback()
                logger.exception("Ошибка сохранения пользователя '%s' в БД", username)
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить пользователя")
                return

            self.accept()
        except Exception:
            logger.exception("Неожиданная ошибка в процессе регистрации '%s'", username)
            QMessageBox.critical(self, "Ошибка", "Внутренняя ошибка регистрации. Подробности в логах.")
        finally:
            db.close()
            SessionLocal.remove()
