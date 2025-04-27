# report_widget.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from db import SessionLocal
from models import Schedule, Homework
from reports import export_pdf, export_excel
from datetime import date

class ReportWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = SessionLocal()
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Заголовок
        lbl = QLabel("Отчёты")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(lbl)

        # Вложенные табы
        tabs = QTabWidget()
        
        # Таб «Расписание»
        self.tab_sched = QWidget()
        tl1 = QVBoxLayout(self.tab_sched)
        self.tbl_sched = QTableWidget()
        tl1.addWidget(self.tbl_sched)
        tabs.addTab(self.tab_sched, "Расписание")

        # Таб «Домашние задания»
        self.tab_hw = QWidget()
        tl2 = QVBoxLayout(self.tab_hw)
        self.tbl_hw = QTableWidget()
        tl2.addWidget(self.tbl_hw)
        tabs.addTab(self.tab_hw, "Домашние задания")

        layout.addWidget(tabs)

        # Кнопки экспорта
        btns = QHBoxLayout()
        self.btn_pdf = QPushButton("Экспорт в PDF")
        self.btn_xlsx = QPushButton("Экспорт в Excel")
        btns.addStretch()
        btns.addWidget(self.btn_pdf)
        btns.addWidget(self.btn_xlsx)
        layout.addLayout(btns)

        # Сигналы
        self.btn_pdf.clicked.connect(self._save_pdf)
        self.btn_xlsx.clicked.connect(self._save_xlsx)

    def _load_data(self):
        # Заполняем таблицу расписания
        lessons = self.db.query(Schedule).order_by(Schedule.date, Schedule.start_time).all()
        headers1 = ["ID", "Дата", "Предмет", "Преподаватель", "Начало", "Конец", "Кабинет", "Тип"]
        self.tbl_sched.setColumnCount(len(headers1))
        self.tbl_sched.setHorizontalHeaderLabels(headers1)
        self.tbl_sched.setRowCount(len(lessons))
        for i, l in enumerate(lessons):
            self.tbl_sched.setItem(i, 0, QTableWidgetItem(str(l.id)))
            self.tbl_sched.setItem(i, 1, QTableWidgetItem(l.date.isoformat()))
            self.tbl_sched.setItem(i, 2, QTableWidgetItem(l.subject))
            self.tbl_sched.setItem(i, 3, QTableWidgetItem(l.teacher))
            self.tbl_sched.setItem(i, 4, QTableWidgetItem(l.start_time.strftime("%H:%M")))
            self.tbl_sched.setItem(i, 5, QTableWidgetItem(l.end_time.strftime("%H:%M")))
            self.tbl_sched.setItem(i, 6, QTableWidgetItem(l.room or ""))
            self.tbl_sched.setItem(i, 7, QTableWidgetItem(l.type))
        self.tbl_sched.resizeColumnsToContents()
        self.tbl_sched.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Таблица домашних заданий
        hws = self.db.query(Homework).order_by(Homework.due_date).all()
        headers2 = ["ID", "Заголовок", "Описание", "Срок", "Состояние", "Файл"]
        self.tbl_hw.setColumnCount(len(headers2))
        self.tbl_hw.setHorizontalHeaderLabels(headers2)
        self.tbl_hw.setRowCount(len(hws))
        today = date.today()
        for i, hw in enumerate(hws):
            status = "Завершено" if hw.due_date and hw.due_date < today else "В процессе"
            self.tbl_hw.setItem(i, 0, QTableWidgetItem(str(hw.id)))
            self.tbl_hw.setItem(i, 1, QTableWidgetItem(hw.title))
            self.tbl_hw.setItem(i, 2, QTableWidgetItem(hw.description or ""))
            self.tbl_hw.setItem(i, 3, QTableWidgetItem(hw.due_date.isoformat() if hw.due_date else ""))
            self.tbl_hw.setItem(i, 4, QTableWidgetItem(status))
            self.tbl_hw.setItem(i, 5, QTableWidgetItem(hw.attachment or ""))
        self.tbl_hw.resizeColumnsToContents()
        self.tbl_hw.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _save_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF", filter="PDF Files (*.pdf)")
        if path:
            export_pdf(path)
            QMessageBox.information(self, "Готово", "PDF-отчёт сохранён")

    def _save_xlsx(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить Excel", filter="Excel Files (*.xlsx)")
        if path:
            export_excel(path)
            QMessageBox.information(self, "Готово", "Excel-отчёт сохранён")
