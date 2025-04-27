# homework_widget.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QScrollArea, QLabel, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from db import SessionLocal
from models import Homework, RoleEnum
from homework_dialog import HomeworkDialog
from datetime import date, timedelta
import os

class HomeworkCard(QFrame):
    def __init__(self, hw: Homework, select_cb, parent=None):
        super().__init__(parent)
        self.hw = hw
        self.hw_id = hw.id
        self.select_cb = select_cb
        self.setObjectName("hwCard")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setProperty("selected", False)
        self._build_ui(hw)

    def _build_ui(self, hw: Homework):
        hl = QHBoxLayout(self)
        hl.setContentsMargins(12, 8, 12, 8)
        hl.setSpacing(16)

        # Текстовые поля
        vl = QVBoxLayout()
        title = QLabel(hw.title);   title.setObjectName("hwTitle")
        due   = hw.due_date.strftime("%d.%m.%Y") if hw.due_date else "-"
        status = ("Закрыто" if hw.due_date and hw.due_date < date.today() else "В процессе")
        lbl_due    = QLabel(f"Срок: {due}");   lbl_due.setObjectName("hwDue")
        lbl_status = QLabel(f"Статус: {status}"); lbl_status.setObjectName("hwStatus")
        vl.addWidget(title); vl.addWidget(lbl_due); vl.addWidget(lbl_status)
        hl.addLayout(vl)

        # Кнопка «Открыть файл», если есть
        if hw.attachment:
            btn_open = QPushButton("Открыть файл")
            btn_open.clicked.connect(self._open_attachment)
            hl.addWidget(btn_open)

        hl.addStretch()

    def mousePressEvent(self, ev):
        self.select_cb(self)
        super().mousePressEvent(ev)

    def _open_attachment(self):
        path = self.hw.attachment
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Ошибка", "Файл не найден")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class HomeworkWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = SessionLocal()
        self.selected_card = None
        self.current_filter = "all"
        self._build_ui()
        self._refresh_content()

    def _build_ui(self):
        self.main_l = QVBoxLayout(self)
        self.main_l.setContentsMargins(16, 16, 16, 16)
        self.main_l.setSpacing(12)

        # CRUD-кнопки только для admin
        if self.user.role == RoleEnum.admin:
            act_l = QHBoxLayout()
            self.btn_add    = QPushButton("Добавить")
            self.btn_edit   = QPushButton("Редактировать")
            self.btn_delete = QPushButton("Удалить")
            act_l.addWidget(self.btn_add)
            act_l.addWidget(self.btn_edit)
            act_l.addWidget(self.btn_delete)
            act_l.addStretch()
            self.main_l.addLayout(act_l)

            self.btn_add.clicked.connect(self._on_add)
            self.btn_edit.clicked.connect(self._on_edit)
            self.btn_delete.clicked.connect(self._on_delete)

        # Фильтры — для всех
        filt_l = QHBoxLayout()
        self.btn_all    = QPushButton("Все")
        self.btn_upc    = QPushButton("Ближайшие")
        self.btn_open   = QPushButton("Открытые")
        self.btn_closed = QPushButton("Закрытые")
        for btn in (self.btn_all, self.btn_upc, self.btn_open, self.btn_closed):
            btn.setCheckable(True)
            btn.setObjectName("filterBtn")
            filt_l.addWidget(btn)
        filt_l.addStretch()
        self.main_l.addLayout(filt_l)
        self.btn_all.setChecked(True)

        self.btn_all.clicked.connect(lambda: self._on_filter("all"))
        self.btn_upc.clicked.connect(lambda: self._on_filter("upc"))
        self.btn_open.clicked.connect(lambda: self._on_filter("open"))
        self.btn_closed.clicked.connect(lambda: self._on_filter("closed"))

        # Секция карточек
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.content_l = QVBoxLayout(self.container)
        self.content_l.setContentsMargins(0,0,0,0); self.content_l.setSpacing(12)
        self.scroll.setWidget(self.container)
        self.main_l.addWidget(self.scroll)

        # Стили
        self.setStyleSheet("""
        QPushButton#filterBtn {
            background-color: #333; color: #ccc; border:none;
            border-radius:12px; padding:4px 16px; font-size:14px;
        }
        QPushButton#filterBtn:hover { background-color: #444; }
        QPushButton#filterBtn:checked { background-color:#2196f3; color:#fff; }

        QFrame#hwCard { background:#333; border-radius:8px; border:2px solid transparent; }
        QFrame#hwCard[selected="true"] { border:2px solid #2196f3; }
        QLabel#hwTitle { font-size:16px; font-weight:bold; color:#fff; }
        QLabel#hwDue, QLabel#hwStatus { font-size:12px; color:#ccc; }
        QPushButton#filterBtn {
            background-color: #333;
            color: #ccc;
            border: none;
            border-radius: 12px;
            padding: 4px 16px;
            font-size: 12px;
        }

        QFrame#emptyCard { background:#222; border-radius:8px; padding:24px; }
        QLabel#emptyIcon { font-size:32px; color:#2196f3; }
        QLabel#emptyTitle { font-size:18px; font-weight:bold; color:#fff; }
        QLabel#emptyText { font-size:12px; color:#aaa; }
        """)

    def _clear_content(self):
        while self.content_l.count():
            item = self.content_l.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()
        self.selected_card = None

    def _on_filter(self, key):
        for btn, k in (
            (self.btn_all,    "all"),
            (self.btn_upc,    "upc"),
            (self.btn_open,   "open"),
            (self.btn_closed, "closed"),
        ):
            btn.setChecked(k == key)
        self.current_filter = key
        self._refresh_content()

    def _refresh_content(self):
        self._clear_content()
        all_hw = self.db.query(Homework).order_by(Homework.due_date).all()
        today  = date.today()

        if self.current_filter == "upc":
            end = today + timedelta(days=7)
            lst = [h for h in all_hw if h.due_date and today <= h.due_date <= end]
        elif self.current_filter == "open":
            lst = [h for h in all_hw if h.due_date and h.due_date >= today]
        elif self.current_filter == "closed":
            lst = [h for h in all_hw if h.due_date and h.due_date < today]
        else:
            lst = all_hw

        if not lst:
            empty = QFrame(); empty.setObjectName("emptyCard")
            vl = QVBoxLayout(empty); vl.setAlignment(Qt.AlignCenter)
            ic = QLabel("📋"); ic.setObjectName("emptyIcon"); vl.addWidget(ic, alignment=Qt.AlignHCenter)
            t  = QLabel("Домашних заданий нет!"); t.setObjectName("emptyTitle"); vl.addWidget(t, alignment=Qt.AlignHCenter)
            txt= QLabel("Нажмите «Добавить», чтобы создать."); txt.setObjectName("emptyText")
            txt.setWordWrap(True); txt.setAlignment(Qt.AlignHCenter); vl.addWidget(txt)
            self.content_l.addWidget(empty)
            self.content_l.addStretch()
            self.scroll.verticalScrollBar().setValue(0)
            return

        for hw in lst:
            card = HomeworkCard(hw, select_cb=self._on_card_selected)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.content_l.addWidget(card)
        self.content_l.addStretch()
        self.scroll.verticalScrollBar().setValue(0)

    def _on_card_selected(self, card):
        if self.selected_card and self.selected_card is not card:
            self.selected_card.setProperty("selected", False)
            self.selected_card.style().unpolish(self.selected_card)
            self.selected_card.style().polish(self.selected_card)
        self.selected_card = card
        card.setProperty("selected", True)
        card.style().unpolish(card)
        card.style().polish(card)

    def _on_add(self):
        dlg = HomeworkDialog(self)
        if dlg.exec_():
            d = dlg.get_data()
            status = "Закрыто" if d["due_date"] < date.today() else "В процессе"
            hw = Homework(**{**d, "status":status})
            self.db.add(hw)
            try:    self.db.commit()
            except: self.db.rollback()
            self._refresh_content()

    def _on_edit(self):
        if not self.selected_card:
            QMessageBox.warning(self, "Ошибка", "Выберите задание")
            return
        hw = self.db.get(Homework, self.selected_card.hw_id)
        dlg = HomeworkDialog(self, hw)
        if dlg.exec_():
            d = dlg.get_data()
            hw.title, hw.description, hw.due_date = d["title"], d["description"], d["due_date"]
            hw.status = "Закрыто" if d["due_date"] < date.today() else "В процессе"
            hw.attachment = d["attachment"]
            try:    self.db.commit()
            except: self.db.rollback()
            self._refresh_content()

    def _on_delete(self):
        if not self.selected_card:
            QMessageBox.warning(self, "Ошибка", "Выберите задание")
            return
        hw = self.db.get(Homework, self.selected_card.hw_id)

        msg = QMessageBox(self)
        msg.setWindowTitle("Подтвердить удаление")
        msg.setText("Вы действительно хотите удалить задание?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        yes_btn = msg.button(QMessageBox.Yes)
        no_btn = msg.button(QMessageBox.No)
        yes_btn.setText("Да")
        no_btn.setText("Нет")
        
        if msg.exec_() == QMessageBox.Yes:
            self.db.delete(hw)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            self._refresh_content()