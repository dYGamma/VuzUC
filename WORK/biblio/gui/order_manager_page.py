from PyQt5 import QtWidgets, QtCore
import controllers
import functools
from datetime import datetime

class OrderManagerPage(QtWidgets.QWidget):
    reload_request = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        # Таблица с 12 колонками: отображение и управление датами
        self.table = QtWidgets.QTableWidget(0, 12)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ученик", "Книга", "Статус", "Заявка",
            "Подтверждение", "Выдача", "Срок сдачи",
            "→ Действие",
            "Установить подтверждение", "Установить выдачу", "Установить срок"
        ])

        btn_refresh = QtWidgets.QPushButton("Обновить")
        btn_refresh.clicked.connect(self.reload)
        layout.addWidget(btn_refresh)
        
        layout.addWidget(self.table)

        self.reload()

    def reload(self):
        self.table.setRowCount(0)
        orders = controllers.list_all_orders()
        for o in orders:
            i = self.table.rowCount()
            self.table.insertRow(i)

            # Отображение основных полей
            values = [
                o.id,
                o.user_id,
                o.book.title,
                o.status,
                o.request_date.strftime("%Y-%m-%d") if o.request_date else "",
                o.confirm_date.strftime("%Y-%m-%d") if getattr(o, 'confirm_date', None) else "",
                o.issue_date.strftime("%Y-%m-%d")   if o.issue_date   else "",
                o.due_date.strftime("%Y-%m-%d")     if getattr(o, 'due_date', None) else ""
            ]
            for col, val in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.table.setItem(i, col, item)

            # Кнопка смены статуса (→)
            btn_action = QtWidgets.QPushButton("→")
            btn_action.clicked.connect(functools.partial(self._next, o.id))
            # Активируем кнопку возврата только если книга выдана и установлены даты
            if o.status == 'issued':
                is_ready = bool(o.issue_date and getattr(o, 'due_date', None))
                btn_action.setEnabled(is_ready)
            else:
                btn_action.setEnabled(True)
            self.table.setCellWidget(i, 8, btn_action)

            # Виджет для установки даты подтверждения
            confirm_date_edit = QtWidgets.QDateEdit()
            confirm_date_edit.setCalendarPopup(True)
            confirm_date_edit.setDate(QtCore.QDate.currentDate())
            btn_set_confirm = QtWidgets.QPushButton("Подтвердить")
            def make_confirm_setter(order_id, widget):
                def setter():
                    d = widget.date().toPyDate()
                    dt = datetime.combine(d, datetime.min.time())
                    try:
                        controllers.set_confirm_date(order_id, dt)
                    except Exception as e:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))
                    self.reload()
                return setter
            btn_set_confirm.clicked.connect(make_confirm_setter(o.id, confirm_date_edit))
            w_conf = QtWidgets.QWidget()
            l_conf = QtWidgets.QHBoxLayout(); l_conf.setContentsMargins(0, 0, 0, 0)
            l_conf.addWidget(confirm_date_edit); l_conf.addWidget(btn_set_confirm)
            w_conf.setLayout(l_conf)
            self.table.setCellWidget(i, 9, w_conf)

            # Виджет для установки даты выдачи
            issue_date_edit = QtWidgets.QDateEdit()
            issue_date_edit.setCalendarPopup(True)
            issue_date_edit.setDate(QtCore.QDate.currentDate())
            btn_set_issue = QtWidgets.QPushButton("Выдать")
            def make_issue_setter(order_id, widget):
                def setter():
                    d = widget.date().toPyDate()
                    dt = datetime.combine(d, datetime.min.time())
                    try:
                        controllers.set_issue_date(order_id, dt)
                    except Exception as e:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))
                    self.reload()
                return setter
            btn_set_issue.clicked.connect(make_issue_setter(o.id, issue_date_edit))
            w_iss = QtWidgets.QWidget()
            l_iss = QtWidgets.QHBoxLayout(); l_iss.setContentsMargins(0, 0, 0, 0)
            l_iss.addWidget(issue_date_edit); l_iss.addWidget(btn_set_issue)
            w_iss.setLayout(l_iss)
            self.table.setCellWidget(i, 10, w_iss)

            # Виджет для установки срока сдачи
            due_date_edit = QtWidgets.QDateEdit()
            due_date_edit.setCalendarPopup(True)
            due_date_edit.setDate(QtCore.QDate.currentDate())
            btn_set_due = QtWidgets.QPushButton("Установить")
            def make_due_setter(order_id, widget):
                def setter():
                    d = widget.date().toPyDate()
                    dt = datetime.combine(d, datetime.min.time())
                    try:
                        controllers.set_due_date(order_id, dt)
                    except Exception as e:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))
                    self.reload()
                return setter
            btn_set_due.clicked.connect(make_due_setter(o.id, due_date_edit))
            w_due = QtWidgets.QWidget()
            l_due = QtWidgets.QHBoxLayout(); l_due.setContentsMargins(0, 0, 0, 0)
            l_due.addWidget(due_date_edit); l_due.addWidget(btn_set_due)
            w_due.setLayout(l_due)
            self.table.setCellWidget(i, 11, w_due)

        self.reload_request.emit()

    def _next(self, order_id):
        try:
            controllers.advance_order(order_id)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(e))
        self.reload()
        self.reload_request.emit()
