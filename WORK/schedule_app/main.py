# main.py

import sys
import os
import logging.config

from PyQt5.QtWidgets import (
    QApplication, QDialog, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLabel, QLineEdit, QDateEdit, QTimeEdit, QComboBox
)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import qtawesome as qta

from db import init_db
from auth_dialog import AuthDialog
from main_window import MainWindow

# Начальная тема
current_theme = 'dark_teal'

# Параметры для каждой темы
theme_params = {
    'dark_teal': {
        'text_color': '#cccccc',
        'input_text_color': '#cccccc',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.moon',
        'label_text': 'Тёмная тема',
    },
    'light_cyan_500': {
        'text_color': '#212121',
        'input_text_color': '#212121',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.sun',
        'label_text': 'Светлая тема',
    },
}

def apply_input_styles():
    """Применяет QSS к полям ввода согласно текущей теме."""
    app = QApplication.instance()
    p = theme_params[current_theme]
    qss = f"""
        QLineEdit, QDateEdit, QTimeEdit, QComboBox {{
            color: {p['input_text_color']};
        }}
        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {{
            color: {p['input_focus_color']};
        }}
        QLineEdit::placeholder {{ color: #888888; }}
        QComboBox QAbstractItemView {{
            color: {p['text_color']};
            background-color: transparent;
            selection-background-color: {p['input_focus_color']};
            selection-color: #ffffff;
        }}
    """
    app.setStyleSheet(app.styleSheet() + qss)

def update_theme_ui(
    theme_btn: QPushButton,
    theme_lbl: QLabel,
    title_lbl: QLabel,
    switch_btn: QPushButton = None,
    username_lbl: QLabel = None
):
    """
    Обновляет:
      - иконку и подпись темы,
      - стиль заголовка,
      - цвет иконки switch_btn и цвет текста username_lbl (если переданы),
      - QSS для полей ввода.
    """
    p = theme_params[current_theme]

    # Текст и иконка темы
    theme_lbl.setText(p['label_text'])
    theme_lbl.setStyleSheet(f"color: {p['text_color']}; font-size: 14px;")
    theme_btn.setIcon(qta.icon(p['icon_name'], color=p['text_color']))

    # Заголовок по центру
    title_lbl.setStyleSheet(f"""
        color: {p['text_color']};
        font-size: 16px;
        font-weight: bold;
        border: 2px solid {p['text_color']};
        padding: 8px;
        border-radius: 8px;
    """)

    # Иконка кнопки смены аккаунта
    if switch_btn:
        switch_btn.setIcon(qta.icon('fa5s.sign-out-alt', color=p['text_color']))

    # Цвет текста логина
    if username_lbl:
        username_lbl.setStyleSheet(f"font-size: 14px; color: {p['text_color']};")

    # Применяем стили к QLineEdit/QDateEdit/QTimeEdit/QComboBox
    apply_input_styles()

def toggle_theme(
    theme_btn: QPushButton,
    theme_lbl: QLabel,
    title_lbl: QLabel,
    switch_btn: QPushButton = None,
    username_lbl: QLabel = None
):
    """Меняет current_theme, перезагружает qt_material и вызывает update_theme_ui."""
    global current_theme
    app = QApplication.instance()

    if current_theme == 'dark_teal':
        apply_stylesheet(app, theme='light_cyan_500.xml')
        current_theme = 'light_cyan_500'
    else:
        apply_stylesheet(app, theme='dark_teal.xml')
        current_theme = 'dark_teal'

    update_theme_ui(theme_btn, theme_lbl, title_lbl, switch_btn, username_lbl)

def setup_ui(window: MainWindow, user):
    """
    Собирает:
      - кнопку смены аккаунта + логин,
      - заголовок,
      - переключатель темы,
      - центральный виджет с вкладками.
    """
    # Верхняя панель
    top_bar = QWidget()
    top_layout = QHBoxLayout(top_bar)
    top_layout.setContentsMargins(16, 8, 16, 8)
    top_layout.setSpacing(8)

    # 1) Кнопка смены аккаунта
    switch_btn = QPushButton()
    switch_btn.setFixedSize(40, 40)

    # 2) Лейбл с логином
    username_lbl = QLabel(user.username)
    username_lbl.setAlignment(Qt.AlignVCenter)

    # 3) Заголовок приложения
    title_lbl = QLabel("Информационная система для управления расписанием учеников")
    title_lbl.setAlignment(Qt.AlignCenter)
    title_lbl.setFixedWidth(700)

    # 4) Блок переключения темы
    toolbar = QWidget()
    tb_layout = QHBoxLayout(toolbar)
    tb_layout.setContentsMargins(0, 0, 0, 0)
    tb_layout.setSpacing(8)
    tb_layout.setAlignment(Qt.AlignRight)
    theme_lbl = QLabel()
    theme_btn = QPushButton()
    theme_btn.setFixedSize(40, 40)
    # при клике передаём все кнопки/лейблы, которые нужно перекрасить
    theme_btn.clicked.connect(
        lambda: toggle_theme(theme_btn, theme_lbl, title_lbl, switch_btn, username_lbl)
    )
    tb_layout.addWidget(theme_lbl)
    tb_layout.addWidget(theme_btn)

    # Собираем верх
    top_layout.addWidget(switch_btn)
    top_layout.addWidget(username_lbl)
    top_layout.addStretch()
    top_layout.addWidget(title_lbl)
    top_layout.addStretch()
    top_layout.addWidget(toolbar)

    # Центральная часть
    central = QWidget()
    main_layout = QVBoxLayout(central)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    if existing := window.centralWidget():
        main_layout.addWidget(top_bar)
        main_layout.addWidget(existing)
    window.setCentralWidget(central)

    # Первоначальная инициализация цветов/иконок
    update_theme_ui(theme_btn, theme_lbl, title_lbl, switch_btn, username_lbl)

    # Callback смены аккаунта
    def on_switch():
        global window
        window.hide()  # прячем текущее окно
        auth = AuthDialog()
        if auth.exec_() == QDialog.Accepted:
            window = MainWindow(auth.user)
            setup_ui(window, auth.user)
            window.show()
        else:
            window.show()  # отмена — возвращаем прежнее окно

    switch_btn.clicked.connect(on_switch)

if __name__ == "__main__":
    # Инициализация БД и логирования
    init_db()
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig('config/log_config.ini', disable_existing_loggers=False)

    # QApplication + начальная тема
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme=f'{current_theme}.xml')
    apply_input_styles()

    # Диалог входа
    auth = AuthDialog()
    if auth.exec_() != QDialog.Accepted:
        sys.exit(0)

    # Первое главное окно
    window = MainWindow(auth.user)
    setup_ui(window, auth.user)
    window.show()

    sys.exit(app.exec_())
