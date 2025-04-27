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
    """
    Применяет стили для полей ввода, полей даты/времени и выпадающих списков
    согласно текущей теме.
    """
    app = QApplication.instance()
    params = theme_params[current_theme]
    qss = f"""
        /* Обычное состояние текстовых полей, даты, времени и комбо */
        QLineEdit,
        QDateEdit,
        QTimeEdit,
        QComboBox {{
            color: {params['input_text_color']};
        }}

        /* Активное (с фокусом) состояние */
        QLineEdit:focus,
        QDateEdit:focus,
        QTimeEdit:focus,
        QComboBox:focus {{
            color: {params['input_focus_color']};
        }}

        /* Плейсхолдер для QLineEdit */
        QLineEdit::placeholder {{
            color: #888888;
        }}

        /* Вид списка выпадающего QComboBox */
        QComboBox QAbstractItemView {{
            color: {params['text_color']};
            background-color: transparent;
            selection-background-color: {params['input_focus_color']};
            selection-color: #ffffff;
        }}
    """
    # Дополним существующий стиль приложения
    app.setStyleSheet(app.styleSheet() + qss)

def update_theme_ui(button: QPushButton, label: QLabel, title_label: QLabel):
    """
    Обновляет заголовок, метку и иконку темы, а затем стили полей ввода.
    """
    params = theme_params[current_theme]

    # Обновляем метку темы
    label.setText(params['label_text'])
    label.setStyleSheet(f"color: {params['text_color']}; font-size: 14px;")

    # Обновляем иконку на кнопке
    button.setIcon(qta.icon(params['icon_name'], color=params['text_color']))

    # Обновляем стиль заголовка
    title_label.setStyleSheet(f"""
        color: {params['text_color']};
        font-size: 16px;
        font-weight: bold;
        border: 2px solid {params['text_color']};
        padding: 8px;
        border-radius: 8px;
    """)

    # Применяем новые стили к полям ввода / дате / времени / комбо
    apply_input_styles()

def toggle_theme(button: QPushButton, label: QLabel, title_label: QLabel):
    """
    Переключает тему и обновляет весь UI.
    """
    global current_theme
    app = QApplication.instance()

    if current_theme == 'dark_teal':
        apply_stylesheet(app, theme='light_cyan_500.xml')
        current_theme = 'light_cyan_500'
    else:
        apply_stylesheet(app, theme='dark_teal.xml')
        current_theme = 'dark_teal'

    update_theme_ui(button, label, title_label)

if __name__ == "__main__":
    # Инициализация БД и логирования
    init_db()
    os.makedirs('logs', exist_ok=True)
    logging.config.fileConfig(
        'config/log_config.ini', disable_existing_loggers=False
    )

    # Создаём приложение и сразу задаём стартовую тему
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme=f'{current_theme}.xml')

    # Сразу применяем стиль для всех полей ввода / дат / времени / комбо
    apply_input_styles()

    # Аутентификация
    auth = AuthDialog()
    if auth.exec_() == QDialog.Accepted:
        window = MainWindow(auth.user)

        # Верхняя панель (заголовок + переключатель темы)
        top_bar = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(16, 8, 16, 8)
        top_layout.setSpacing(8)
        top_bar.setLayout(top_layout)

        title_label = QLabel("Информационная система для управления расписанием учеников")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFixedWidth(700)

        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(8)
        toolbar_layout.setAlignment(Qt.AlignRight)
        toolbar.setLayout(toolbar_layout)

        theme_label = QLabel()
        toolbar_layout.addWidget(theme_label)

        theme_btn = QPushButton()
        theme_btn.setFixedSize(40, 40)
        theme_btn.clicked.connect(lambda: toggle_theme(theme_btn, theme_label, title_label))
        toolbar_layout.addWidget(theme_btn)

        top_layout.addStretch()
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(toolbar)

        # Собираем центральный виджет
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(top_bar)
        if existing := window.centralWidget():
            main_layout.addWidget(existing)
        central.setLayout(main_layout)
        window.setCentralWidget(central)

        # Инициализация UI в текущей теме
        update_theme_ui(theme_btn, theme_label, title_label)

        window.show()
        sys.exit(app.exec_())
