from PyQt5 import QtWidgets, QtCore
from utils.theme_manager import toggle_theme, update_theme_ui
from gui.book_manager_page import BookManagerPage
from gui.order_manager_page import OrderManagerPage
from gui.report_page import ReportPage
from gui.user_manager_page import UserManagerPage
from gui.librarian_manager_page import LibrarianManagerPage
from gui.student_page import StudentPage
import logging

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user, make_login_dialog):
        super().__init__()
        self.user = user
        self.make_login_dialog = make_login_dialog

        # Окно
        self.setWindowTitle(f"Школьная библиотека — {user.role.capitalize()}")
        self.resize(1024, 768)

        # Навигатор слева
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.setFixedWidth(180)
        self.stack = QtWidgets.QStackedWidget()

        if user.role == 'student':
            # Студент: поиск и мои заказы — внутри StudentPage
            self.nav_list.addItem("🔍 Поиск и Заказы")
            self.page_student = StudentPage(user.id)
            self.stack.addWidget(self.page_student)
        else:
            # Общие разделы для librarian/admin
            self.nav_list.addItem("📚 Каталог книг")
            self.page_books   = BookManagerPage()
            self.stack.addWidget(self.page_books)

            self.nav_list.addItem("🔖 Заказы")
            self.page_orders  = OrderManagerPage()
            self.stack.addWidget(self.page_orders)

            self.nav_list.addItem("📑 Отчёты")
            self.page_reports = ReportPage()
            self.stack.addWidget(self.page_reports)
            # НУЖНА ПРАВКА!!!
            if user.role == 'librarian':
                self.nav_list.addItem("👥 Пользователи")
                self.page_users = UserManagerPage()
                self.stack.addWidget(self.page_users)

            if user.role == 'admin':
                self.nav_list.addItem("🛠 Библиотекари")
                self.page_libs = LibrarianManagerPage()
                self.stack.addWidget(self.page_libs)

            # при изменении каталога обновлять заказы
            self.page_books.data_changed.connect(self.page_orders.reload)

        self.nav_list.currentRowChanged.connect(self.on_nav_changed)

        # Верхний тулбар
        top_bar = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(top_bar)
        hl.setContentsMargins(8,8,8,4)
        hl.setSpacing(4)

        lbl_title = QtWidgets.QLabel("Панель управления библиотекой")
        lbl_title.setAlignment(QtCore.Qt.AlignCenter)

        btn_switch = QtWidgets.QPushButton()
        btn_switch.setFixedSize(32,32)
        btn_switch.clicked.connect(self.on_switch_account)

        btn_theme = QtWidgets.QPushButton()
        btn_theme.setFixedSize(32,32)
        btn_theme.clicked.connect(lambda: toggle_theme(btn_theme, lbl_title, btn_switch))

        update_theme_ui(btn_theme, lbl_title, btn_switch)

        hl.addStretch()
        hl.addWidget(lbl_title, stretch=1)
        hl.addStretch()

        right_vbox = QtWidgets.QVBoxLayout()
        right_vbox.setSpacing(4)
        right_vbox.addWidget(btn_switch, alignment=QtCore.Qt.AlignRight)
        right_vbox.addWidget(btn_theme,  alignment=QtCore.Qt.AlignRight)
        right_vbox.addStretch()

        rc = QtWidgets.QWidget()
        rc.setLayout(right_vbox)
        hl.addWidget(rc, 0, QtCore.Qt.AlignRight)

        central = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(central)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)
        vbox.addWidget(top_bar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.nav_list)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1,1)
        vbox.addWidget(splitter)

        self.setCentralWidget(central)

        # Показываем первую вкладку
        self.nav_list.setCurrentRow(0)
        logger.info("MainWindow initialized for %s", user.id)

    def on_nav_changed(self, index: int):
        self.stack.setCurrentIndex(index)

    def on_switch_account(self):
        self.hide()
        dlg = self.make_login_dialog()
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            new_user = dlg.user
            logger.info("Switching to %s", new_user.id)
            win = MainWindow(new_user, self.make_login_dialog)
            win.show()
        else:
            self.show()
