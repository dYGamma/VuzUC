# homework_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDateEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QDate

class HomeworkDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать домашнее задание")
        self.resize(400, 300)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Заголовок:"))
        self.edit_title = QLineEdit()
        layout.addWidget(self.edit_title)

        layout.addWidget(QLabel("Описание:"))
        self.edit_desc = QTextEdit()
        layout.addWidget(self.edit_desc)

        layout.addWidget(QLabel("Срок выполнения:"))
        self.date_due = QDateEdit()
        self.date_due.setCalendarPopup(True)
        self.date_due.setDate(QDate.currentDate())
        layout.addWidget(self.date_due)

        attach_layout = QHBoxLayout()
        self.edit_attach = QLineEdit()
        self.btn_browse  = QPushButton("Обзор")
        attach_layout.addWidget(self.edit_attach)
        attach_layout.addWidget(self.btn_browse)
        layout.addWidget(QLabel("Прикрепить файл:"))
        layout.addLayout(attach_layout)

        self.btn_browse.clicked.connect(self.browse_file)

        btns = QHBoxLayout()
        self.btn_ok     = QPushButton("Сохранить")
        self.btn_cancel = QPushButton("Отмена")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self._on_ok)
        self.btn_cancel.clicked.connect(self.reject)

        if data:
            self.edit_title.setText(data.title)
            self.edit_desc.setPlainText(data.description or "")
            self.date_due.setDate(QDate(
                data.due_date.year, data.due_date.month, data.due_date.day
            ))
            self.edit_attach.setText(data.attachment or "")

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        if path:
            self.edit_attach.setText(path)

    def _on_ok(self):
        if not self.edit_title.text().strip():
            QMessageBox.warning(self, "Ошибка", "Укажите заголовок задания")
            return
        # можно добавить валидацию на описание/файл, если нужно
        self.accept()

    def get_data(self):
        return {
            "title":       self.edit_title.text().strip(),
            "description": self.edit_desc.toPlainText().strip(),
            "due_date":    self.date_due.date().toPyDate(),
            "attachment":  self.edit_attach.text().strip()
        }
