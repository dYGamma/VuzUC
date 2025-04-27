# user_dialog.py
import re
import logging
import bcrypt

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from db import SessionLocal
from models import User, RoleEnum

logger = logging.getLogger(__name__)

# Соответствие enum → русская строка
ROLE_RU = {
    RoleEnum.student: 'Ученик',
    RoleEnum.parent:  'Родитель',
    RoleEnum.admin:   'Администратор',
}

class UserDialog(QDialog):
    """
    Диалог для создания или редактирования пользователя.
    Если user=None — создание, иначе — редактирование.
    """
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Редактирование пользователя" if user else "Добавление пользователя")
        self.resize(350, 260)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Имя пользователя (3–30 символов):"))
        self.edit_login = QLineEdit()
        layout.addWidget(self.edit_login)

        layout.addWidget(QLabel("Роль:"))
        self.combo_role = QComboBox()
        # Заполняем список ролей по-русски
        for role in RoleEnum:
            self.combo_role.addItem(ROLE_RU[role], role)
        layout.addWidget(self.combo_role)

        layout.addWidget(QLabel("Новый пароль:"))
        self.edit_pass = QLineEdit()
        self.edit_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass)

        layout.addWidget(QLabel("Подтвердите пароль:"))
        self.edit_pass2 = QLineEdit()
        self.edit_pass2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.edit_pass2)

        if user:
            note = QLabel("Оставьте поля пароля пустыми, чтобы не менять старый")
            note.setStyleSheet("color: gray; font-size: 10px;")
            layout.addWidget(note)
            # Заполняем поля для редактирования
            self.edit_login.setText(user.username)
            idx = self.combo_role.findData(user.role)
            if idx >= 0:
                self.combo_role.setCurrentIndex(idx)

        self.btn_save = QPushButton("Сохранить")
        self.btn_cancel = QPushButton("Отмена")
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_cancel)

        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_username(self, username: str) -> bool:
        return bool(re.match(r'^[A-Za-z0-9_]{3,30}$', username))

    def validate_password(self, pw: str) -> bool:
        if len(pw) < 8 or not re.search(r"[A-Z]", pw) \
           or not re.search(r"[a-z]", pw) or not re.search(r"\d", pw) \
           or not re.search(r"[^A-Za-z0-9]", pw):
            return False
        return True

    def on_save(self):
        username = self.edit_login.text().strip()
        pw1 = self.edit_pass.text()
        pw2 = self.edit_pass2.text()
        role = self.combo_role.currentData()

        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите имя пользователя")
            return
        if not self.validate_username(username):
            QMessageBox.warning(self, "Ошибка", "Логин: 3–30 символов, буквы/цифры/_")
            return

        # При редактировании пароль можно не менять
        if self.user is None or pw1 or pw2:
            if pw1 != pw2:
                QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
                return
            if not self.validate_password(pw1):
                QMessageBox.warning(
                    self, "Ошибка",
                    "Пароль должен быть ≥8 символов и содержать:\n"
                    "Заглавную, строчную букву, цифру и спецсимвол"
                )
                return

        db = SessionLocal()
        try:
            if self.user is None:
                if db.query(User).filter_by(username=username).first():
                    QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
                    return
                pw_hash = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt()).decode()
                new_user = User(username=username, password_hash=pw_hash, role=role)
                db.add(new_user)
            else:
                u = db.query(User).get(self.user.id)
                if not u:
                    QMessageBox.critical(self, "Ошибка", "Пользователь не найден")
                    return
                u.username = username
                u.role = role
                if pw1:
                    u.password_hash = bcrypt.hashpw(pw1.encode(), bcrypt.gensalt()).decode()

            db.commit()
            self.accept()
        except Exception:
            db.rollback()
            logger.exception("Ошибка сохранения пользователя")
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить пользователя")
        finally:
            db.close()
