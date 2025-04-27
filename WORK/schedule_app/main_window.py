# main_window.py
import logging
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from schedule_widget import ScheduleWidget
from homework_widget import HomeworkWidget
from report_widget import ReportWidget
from notifications import NotificationManager
from models import RoleEnum
from user_management_widget import UserManagementWidget

ROLE_RU = {
    RoleEnum.student: 'Ученик',
    RoleEnum.parent:  'Родитель',
    RoleEnum.admin:   'Администратор'
}

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        role_text = ROLE_RU.get(user.role, user.role.value)
        self.setWindowTitle(f"Менеджер расписания — {user.username} ({role_text})")
        self.resize(900, 650)

        tabs = QTabWidget()

        # Распределяем вкладки по ролям
        if user.role == RoleEnum.student:
            tabs.addTab(ScheduleWidget(user), "Расписание")
            tabs.addTab(HomeworkWidget(user), "Домашние задания")
        elif user.role == RoleEnum.parent:
            tabs.addTab(ScheduleWidget(user), "Расписание")
            tabs.addTab(ReportWidget(user),   "Отчёты")
        elif user.role == RoleEnum.admin:
            tabs.addTab(ScheduleWidget(user), "Расписание")
            tabs.addTab(HomeworkWidget(user),"Домашние задания")
            tabs.addTab(ReportWidget(user),   "Отчёты")
            tabs.addTab(UserManagementWidget(), "Пользователи")

        self.setCentralWidget(tabs)

        logger = logging.getLogger(__name__)
        logger.info(f"Пользователь {user.username} ({role_text}) вошёл в систему.")

        # Запуск службы уведомлений
        notif = NotificationManager()
        notif.start()
