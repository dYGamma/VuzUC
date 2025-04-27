# schedule_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QDateEdit, QTimeEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QDate
from datetime import datetime

class ScheduleDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить/Редактировать занятие")
        self.resize(360, 320)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Предмет:"))
        self.edit_subject = QLineEdit()
        layout.addWidget(self.edit_subject)

        layout.addWidget(QLabel("Преподаватель:"))
        self.edit_teacher = QLineEdit()
        layout.addWidget(self.edit_teacher)

        layout.addWidget(QLabel("Дата занятия:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        htime = QHBoxLayout()
        htime.addWidget(QLabel("Начало:"))
        self.time_start = QTimeEdit()
        self.time_start.setDisplayFormat("HH:mm")
        self.time_start.setTime(self.time_start.time())  # текущее время
        htime.addWidget(self.time_start)

        htime.addWidget(QLabel("Конец:"))
        self.time_end = QTimeEdit()
        self.time_end.setDisplayFormat("HH:mm")
        self.time_end.setTime(self.time_start.time().addSecs(3600))
        htime.addWidget(self.time_end)
        layout.addLayout(htime)

        layout.addWidget(QLabel("Кабинет:"))
        self.edit_room = QLineEdit()
        layout.addWidget(self.edit_room)

        layout.addWidget(QLabel("Тип занятия:"))
        from PyQt5.QtWidgets import QComboBox
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Лекция", "Практика", "Семинар"])
        layout.addWidget(self.combo_type)

        btns = QHBoxLayout()
        self.btn_ok     = QPushButton("Сохранить")
        self.btn_cancel = QPushButton("Отмена")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self._on_ok)
        self.btn_cancel.clicked.connect(self.reject)

        if data:
            # при редактировании заполняем поля из data
            self.edit_subject.setText(data.subject)
            self.edit_teacher.setText(data.teacher)
            self.date_edit.setDate(QDate(data.date.year, data.date.month, data.date.day))
            self.time_start.setTime(datetime.strptime(data.start_time.strftime("%H:%M"), "%H:%M").time())
            self.time_end.setTime(datetime.strptime(data.end_time.strftime("%H:%M"), "%H:%M").time())
            self.edit_room.setText(data.room or "")
            idx = self.combo_type.findText(data.type)
            if idx >= 0:
                self.combo_type.setCurrentIndex(idx)

    def _on_ok(self):
        # простая валидация
        if not self.edit_subject.text().strip():
            QMessageBox.warning(self, "Ошибка", "Укажите предмет")
            return
        if self.time_end.time() <= self.time_start.time():
            QMessageBox.warning(self, "Ошибка", "Время конца должно быть позже начала")
            return
        self.accept()

    def get_data(self):
        """Возвращает dict для создания/обновления Schedule."""
        return {
            "subject":    self.edit_subject.text().strip(),
            "teacher":    self.edit_teacher.text().strip(),
            "date":       self.date_edit.date().toPyDate(),
            "start_time": self.time_start.time().toString("HH:mm"),
            "end_time":   self.time_end.time().toString("HH:mm"),
            "room":       self.edit_room.text().strip(),
            "type":       self.combo_type.currentText()
        }
