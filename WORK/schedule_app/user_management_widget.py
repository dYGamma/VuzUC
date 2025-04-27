# user_management_widget.py
import logging

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView
)
from db import SessionLocal
from models import User, RoleEnum
from user_dialog import UserDialog

logger = logging.getLogger(__name__)

ROLE_RU = {
    RoleEnum.student: 'Ученик',
    RoleEnum.parent:  'Родитель',
    RoleEnum.admin:   'Администратор',
}

class UserManagementWidget(QWidget):
    """
    Виджет для администрирования пользователей: Добавить, Редактировать, Удалить.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Таблица пользователей
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        layout.addWidget(self.table)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        for btn in (self.btn_add, self.btn_edit, self.btn_delete):
            btn.setMinimumWidth(100)
            btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Сигналы
        self.btn_add.clicked.connect(self.add_user)
        self.btn_edit.clicked.connect(self.edit_user)
        self.btn_delete.clicked.connect(self.delete_user)

        self.load_users()

    def load_users(self):
        """
        Загружает всех пользователей в таблицу.
        """
        db = SessionLocal()
        try:
            users = db.query(User).order_by(User.id).all()
            self.table.setRowCount(0)
            for u in users:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(u.id)))
                self.table.setItem(row, 1, QTableWidgetItem(u.username))
                role_name = ROLE_RU.get(u.role, u.role.value)
                self.table.setItem(row, 2, QTableWidgetItem(role_name))
        except Exception:
            logger.exception("Ошибка загрузки пользователей")
        finally:
            db.close()

    def get_selected_user_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        try:
            return int(item.text())
        except Exception:
            return None

    def add_user(self):
        dlg = UserDialog(self, None)
        if dlg.exec_() == dlg.Accepted:
            self.load_users()

    def edit_user(self):
        uid = self.get_selected_user_id()
        if uid is None:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования")
            return
        db = SessionLocal()
        try:
            u = db.query(User).get(uid)
        finally:
            db.close()
        if not u:
            QMessageBox.critical(self, "Ошибка", f"Пользователь ID={uid} не найден")
            return
        dlg = UserDialog(self, u)
        if dlg.exec_() == dlg.Accepted:
            self.load_users()

    def delete_user(self):
        uid = self.get_selected_user_id()
        if uid is None:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        # Создаем сообщение
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение удаления")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText(f"Вы уверены, что хотите удалить пользователя <b>ID={uid}</b>?")
        msg_box.setStandardButtons(QMessageBox.NoButton)  # убираем стандартные кнопки

        # Кнопки "Да" и "Нет"
        btn_yes = QPushButton("Да")
        btn_no = QPushButton("Нет")
        msg_box.addButton(btn_yes, QMessageBox.YesRole)
        msg_box.addButton(btn_no, QMessageBox.NoRole)

        # По умолчанию выделяем кнопку "Да"
        msg_box.setDefaultButton(btn_yes)

        result = msg_box.exec_()

        if result != 0:  # Если не "Да" — отменяем
            return

        db = SessionLocal()
        try:
            u = db.query(User).get(uid)
            if not u:
                QMessageBox.critical(self, "Ошибка", "Пользователь не найден")
                return
            db.delete(u)
            db.commit()
            self.load_users()
        except Exception:
            db.rollback()
            logger.exception("Ошибка удаления пользователя")
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить пользователя")
        finally:
            db.close()
