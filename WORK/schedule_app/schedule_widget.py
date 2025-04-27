# schedule_widget.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame,
    QHBoxLayout, QSizePolicy, QPushButton, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPalette
from db import SessionLocal
from models import Schedule, RoleEnum
from schedule_dialog import ScheduleDialog
from datetime import datetime
from itertools import groupby

MONTHS_RU = {
    'January': 'Января',
    'February': 'Февраля',
    'March': 'Марта',
    'April': 'Апреля',
    'May': 'Мая',
    'June': 'Июня',
    'July': 'Июля',
    'August': 'Августа',
    'September': 'Сентября',
    'October': 'Октября',
    'November': 'Ноября',
    'December': 'Декабря'
}


class LessonCard(QFrame):
    def __init__(self, lesson: Schedule, select_cb, parent=None):
        super().__init__(parent)
        self.lesson_id = lesson.id
        self.select_cb = select_cb
        self.setObjectName("lessonCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setProperty("selected", False)
        self._build_ui(lesson)

    def _build_ui(self, l: Schedule):
        hl = QHBoxLayout(self)
        hl.setContentsMargins(8, 8, 8, 8)
        hl.setSpacing(12)

        # время
        from PyQt5.QtWidgets import QVBoxLayout
        vl_time = QVBoxLayout()
        lbl_start = QLabel(l.start_time.strftime("%H:%M"))
        lbl_end   = QLabel(l.end_time.strftime("%H:%M"))
        lbl_start.setObjectName("timeLabel")
        lbl_end.setObjectName("timeLabelSmall")
        vl_time.addWidget(lbl_start)
        vl_time.addWidget(lbl_end)
        vl_time.addStretch()
        hl.addLayout(vl_time)

        # основное
        vl_main = QVBoxLayout()
        lbl_type  = QLabel(l.type)
        lbl_type.setObjectName("typeLabel")
        lbl_title = QLabel(l.subject)
        lbl_title.setObjectName("titleLabel")
        vl_main.addWidget(lbl_type)
        vl_main.addWidget(lbl_title)

        lbl_room = QLabel(f"Каб. {l.room or '-'}")
        lbl_room.setObjectName("roomLabel")
        lbl_teacher = QLabel(l.teacher)
        lbl_teacher.setObjectName("teacherLabel")
        vl_main.addWidget(lbl_room)
        vl_main.addWidget(lbl_teacher)

        hl.addLayout(vl_main)
        hl.addStretch()

    def mousePressEvent(self, ev):
        self.select_cb(self)
        super().mousePressEvent(ev)


class ScheduleWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = SessionLocal()
        self.selected_card = None
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.main_l = QVBoxLayout(self)
        self.main_l.setContentsMargins(16, 16, 16, 16)
        self.main_l.setSpacing(12)

        # CRUD-кнопки только для admin
        if self.user.role == RoleEnum.admin:
            top = QHBoxLayout()
            self.btn_add  = QPushButton("Добавить")
            self.btn_edit = QPushButton("Редактировать")
            self.btn_del  = QPushButton("Удалить")
            top.addWidget(self.btn_add)
            top.addWidget(self.btn_edit)
            top.addWidget(self.btn_del)
            top.addStretch()
            self.main_l.addLayout(top)

            self.btn_add.clicked.connect(self.on_add)
            self.btn_edit.clicked.connect(self.on_edit)
            self.btn_del.clicked.connect(self.on_delete)

        # Скролл-секция
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.vl = QVBoxLayout(self.container)
        self.vl.setContentsMargins(0, 0, 0, 0)
        self.vl.setSpacing(16)
        self.scroll.setWidget(self.container)
        self.main_l.addWidget(self.scroll)

        # Стили для карточек (без заголовков дней)
        self.setStyleSheet("""
        QFrame#lessonCard {
            background-color: #333;
            border-radius: 8px;
            border: 2px solid transparent;
        }
        QFrame#lessonCard[selected="true"] {
            border: 2px solid #2196f3;
        }
        #timeLabel {
            font-size: 18px;
            color: #fff;
        }
        #timeLabelSmall {
            font-size: 12px;
            color: #aaa;
        }
        #typeLabel {
            font-size: 14px;
            color: #9c27b0;
        }
        #titleLabel {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
        }
        #roomLabel, #teacherLabel {
            font-size: 12px;
            color: #ccc;
        }
        QLabel#empty {
            font-size: 14px;
            color: #fff;
            margin: 20px;
        }
        """)

    def refresh(self):
        # Удаляем старые виджеты
        for i in reversed(range(self.vl.count())):
            w = self.vl.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.selected_card = None

        # Получаем расписание
        lessons = (
            self.db.query(Schedule)
            .order_by(Schedule.date, Schedule.start_time)
            .all()
        )

        if not lessons:
            lbl = QLabel("Расписание пусто.")
            lbl.setObjectName("empty")
            lbl.setAlignment(Qt.AlignCenter)
            self.vl.addWidget(lbl)
            self.vl.addStretch()
            return

        # Группируем и рисуем
        for day, group in groupby(lessons, lambda l: l.date):
            # Переводим день и месяц
            ru_day = {
                "Monday":"Понедельник","Tuesday":"Вторник","Wednesday":"Среда",
                "Thursday":"Четверг","Friday":"Пятница","Saturday":"Суббота","Sunday":"Воскресенье"
            }[day.strftime("%A")]
            ru_month = MONTHS_RU[day.strftime('%B')]

            # Создаём заголовок дня
            hdr = QLabel(f"{ru_day}, {day.day} {ru_month}")
            hdr.setObjectName("dayHeader")
            hdr.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Устанавливаем цвет и шрифт из палитры
            hdr.setStyleSheet(
                "color: #00bcd4; font-size: 18px; font-weight: bold;"
            )

            self.vl.addWidget(hdr)

            # Карточки уроков
            for lesson in group:
                card = LessonCard(lesson, select_cb=self._on_card_selected)
                card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.vl.addWidget(card)

        self.vl.addStretch()

    def changeEvent(self, event):
        super().changeEvent(event)
        # При смене палитры (темы) обновляем цвет всех заголовков дней
        if event.type() == QEvent.PaletteChange:
            for i in range(self.vl.count()):
                w = self.vl.itemAt(i).widget()
                if isinstance(w, QLabel) and w.objectName() == "dayHeader":
                    # Принудительно устанавливаем цвет циановый (#00bcd4)
                    w.setStyleSheet(
                        f"color: #00bcd4; font-size: 18px; font-weight: bold;"
                    )

    def _on_card_selected(self, card: LessonCard):
        if self.selected_card and self.selected_card is not card:
            self.selected_card.setProperty("selected", False)
            self.selected_card.style().unpolish(self.selected_card)
            self.selected_card.style().polish(self.selected_card)
        self.selected_card = card
        card.setProperty("selected", True)
        card.style().unpolish(card)
        card.style().polish(card)

    def on_add(self):
        dlg = ScheduleDialog(self)
        if dlg.exec_():
            data = dlg.get_data()
            from datetime import datetime
            s = Schedule(
                subject    = data["subject"],
                teacher    = data["teacher"],
                date       = data["date"],
                start_time = datetime.strptime(data["start_time"], "%H:%M").time(),
                end_time   = datetime.strptime(data["end_time"],   "%H:%M").time(),
                room       = data["room"],
                type       = data["type"]
            )
            self.db.add(s)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            self.refresh()

    def on_edit(self):
        if not self.selected_card:
            QMessageBox.warning(self, "Ошибка", "Выберите занятие")
            return
        sid = self.selected_card.lesson_id
        s = self.db.get(Schedule, sid)
        dlg = ScheduleDialog(self, s)
        if dlg.exec_():
            d = dlg.get_data()
            from datetime import datetime
            s.subject    = d["subject"]
            s.teacher    = d["teacher"]
            s.date       = d["date"]
            s.start_time = datetime.strptime(d["start_time"], "%H:%M").time()
            s.end_time   = datetime.strptime(d["end_time"],   "%H:%M").time()
            s.room       = d["room"]
            s.type       = d["type"]
            try:
                self.db.commit()
            except:
                self.db.rollback()
            self.refresh()

    def on_delete(self):
        if not self.selected_card:
            QMessageBox.warning(self, "Ошибка", "Выберите занятие")
            return
        sid = self.selected_card.lesson_id
        s = self.db.get(Schedule, sid)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Вы действительно хотите удалить занятие?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Сначала показать окно
        msg_box.show()

        # Потом заменить текст на кнопках
        msg_box.button(QMessageBox.Yes).setText("Да")
        msg_box.button(QMessageBox.No).setText("Нет")

        # Ждать ответ пользователя
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            self.db.delete(s)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            self.refresh()