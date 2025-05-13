import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,
                             QPushButton,QTableWidget,QTableWidgetItem,QGroupBox,
                             QFormLayout,QLineEdit,QDateTimeEdit,QDoubleSpinBox,
                             QFileDialog,QMessageBox,QStackedWidget,QHeaderView)
from PyQt5.QtCore import Qt,QDateTime
import sqlite3


class SalesManagementWindow(QWidget):
    def __init__(self,previous_window,login_window,username):
        super().__init__()
        self.setWindowTitle("Управление продажами")
        self.showFullScreen()
        self.previous_window = previous_window
        self.login_window = login_window
        self.username = username
        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS sales
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                product_name
                                TEXT
                                NOT
                                NULL,
                                saler_name
                                TEXT
                                NOT
                                NULL,
                                region
                                TEXT
                                NOT
                                NULL,
                                date
                                TEXT
                                NOT
                                NULL,
                                price
                                REAL
                                NOT
                                NULL
                            )
                            ''')
        self.conn.commit()

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QTableWidget {
                font-size: 12px;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
            }
            QPushButton {
                min-height: 35px;
                padding: 5px 10px;
                background-color: #0078d4;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #006cbd;
            }
            QLineEdit, QDateTimeEdit, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QLabel {
                margin: 5px 0;
            }
        """)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Top bar
        top_bar = QHBoxLayout()
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        top_bar.addWidget(back_button)

        top_bar.addStretch()
        top_bar.addWidget(QLabel(f"Пользователь: {self.username}"))
        main_layout.addLayout(top_bar)

        # Main content
        content_layout = QHBoxLayout()

        # Table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["ID","Название","Продавец","Регион","Дата","Цена"]
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.cellChanged.connect(self.on_cell_changed)

        # Stacked widgets
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedWidth(350)

        self.init_panels()

        content_layout.addWidget(self.table_widget,70)
        content_layout.addWidget(self.create_buttons_panel(),15)
        content_layout.addWidget(self.stacked_widget,15)

        main_layout.addLayout(content_layout)
        self.refresh_table()

    def create_button(self,text,handler):
        btn = QPushButton(text)
        btn.clicked.connect(handler)
        return btn

    def create_buttons_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5,0,5,0)

        buttons = [
            ("Добавить",self.show_add_panel),
            ("Поиск",self.show_search_panel),
            ("Редактировать",self.show_edit_panel),
            ("Экспорт",self.export_to_excel),
            ("Импорт",self.import_from_excel),
            ("Очистить",self.clear_all_sales)
        ]

        for text,handler in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def init_panels(self):
        # Add panel
        self.add_panel = self.create_add_panel()
        self.stacked_widget.addWidget(self.add_panel)

        # Search panel
        self.search_panel = self.create_search_panel()
        self.stacked_widget.addWidget(self.search_panel)

        # Edit panel
        self.edit_panel = self.create_edit_panel()
        self.stacked_widget.addWidget(self.edit_panel)

        # Empty panel
        self.empty_panel = QWidget()
        self.stacked_widget.addWidget(self.empty_panel)
        self.stacked_widget.setCurrentWidget(self.empty_panel)

    def create_add_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.add_product_name = QLineEdit()
        self.add_saler_name = QLineEdit()
        self.add_region = QLineEdit()
        self.add_date = QDateTimeEdit()
        self.add_date.setDisplayFormat("dd.MM.yyyy")
        self.add_date.setDateTime(QDateTime.currentDateTime())
        self.add_price = QDoubleSpinBox()
        self.add_price.setMaximum(999999)

        form = QFormLayout()
        form.addRow("Название:",self.add_product_name)
        form.addRow("Продавец:",self.add_saler_name)
        form.addRow("Регион:",self.add_region)
        form.addRow("Дата:",self.add_date)
        form.addRow("Цена:",self.add_price)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.save_record)
        btn_clear = QPushButton("Очистить")
        btn_clear.clicked.connect(self.clear_add_form)

        layout.addLayout(form)
        layout.addWidget(btn_save)
        layout.addWidget(btn_clear)
        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def create_search_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.search_id = QLineEdit()
        self.search_product = QLineEdit()
        self.search_saler = QLineEdit()

        form = QFormLayout()
        form.addRow("ID:",self.search_id)
        form.addRow("Название:",self.search_product)
        form.addRow("Продавец:",self.search_saler)

        btn_search = self.create_button("Найти",self.search_records)
        btn_clear = self.create_button("Сброс",self.clear_search_form)

        layout.addLayout(form)
        layout.addWidget(btn_search)
        layout.addWidget(btn_clear)
        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def create_edit_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()

        self.edit_id = QLineEdit()
        self.edit_product = QLineEdit()
        self.edit_saler = QLineEdit()
        self.edit_region = QLineEdit()
        self.edit_date = QDateTimeEdit()
        self.edit_date.setDisplayFormat("dd.MM.yyyy")
        self.edit_price = QDoubleSpinBox()
        self.edit_price.setMaximum(999999)

        form = QFormLayout()
        form.addRow("ID:",self.edit_id)
        form.addRow("Название:",self.edit_product)
        form.addRow("Продавец:",self.edit_saler)
        form.addRow("Регион:",self.edit_region)
        form.addRow("Дата:",self.edit_date)
        form.addRow("Цена:",self.edit_price)

        btn_frame = QHBoxLayout()
        btn_save = self.create_button("Сохранить",self.save_edit)
        btn_delete = self.create_button("Удалить",self.delete_record)

        btn_frame.addWidget(btn_save)
        btn_frame.addWidget(btn_delete)

        layout.addLayout(form)
        layout.addLayout(btn_frame)
        layout.addStretch()

        panel.setLayout(layout)
        return panel

    def show_add_panel(self):
        self.stacked_widget.setCurrentWidget(self.add_panel)
        self.clear_add_form()

    def show_search_panel(self):
        self.stacked_widget.setCurrentWidget(self.search_panel)
        self.clear_search_form()

    def show_edit_panel(self):
        self.stacked_widget.setCurrentWidget(self.edit_panel)
        self.clear_edit_form()

    def refresh_table(self):
        self.table_widget.setRowCount(0)
        query = "SELECT * FROM sales"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        self.table_widget.setRowCount(len(data))
        for row_idx,row_data in enumerate(data):
            for col_idx,value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_idx == 0:  # ID только для чтения
                    item.setFlags(Qt.ItemIsEnabled)
                self.table_widget.setItem(row_idx,col_idx,item)

    def on_cell_changed(self, row, column):
        try:
            if column == 0:  # Не разрешаем редактировать ID
                return

            item_id = int(self.table_widget.item(row, 0).text())
            column_name = self.table_widget.horizontalHeaderItem(column).text()
            new_value = self.table_widget.item(row, column).text()

            column_mapping = {
                "Название": "product_name",
                "Продавец": "saler_name",
                "Регион": "region",
                "Дата": "date",
                "Цена": "price"
            }

            # Преобразование для даты
            if column == 4:
                new_value = QDateTime.fromString(new_value, "dd.MM.yyyy").toString("dd.MM.yyyy")

            if column_name in column_mapping:
                self.cursor.execute(f'''
                    UPDATE sales 
                    SET {column_mapping[column_name]} = ? 
                    WHERE id = ?
                ''', (new_value, item_id))
                self.conn.commit()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")
            self.refresh_table()

    def save_record(self):
        try:
            self.cursor.execute('''
                                INSERT INTO sales (product_name, saler_name, region, date, price)
                                VALUES (?, ?, ?, ?, ?)
                                ''',(
                                    self.add_product_name.text(),
                                    self.add_saler_name.text(),
                                    self.add_region.text(),
                                    self.add_date.text(),
                                    self.add_price.value()
                                ))
            self.conn.commit()
            self.refresh_table()
            self.clear_add_form()
            QMessageBox.information(self,"Успех","Запись успешно добавлена")
        except Exception as e:
            QMessageBox.critical(self,"Ошибка",f"Ошибка сохранения: {str(e)}")

    def search_records(self):
        conditions = []
        params = []

        if self.search_id.text():
            conditions.append("id = ?")
            params.append(self.search_id.text())
        if self.search_product.text():
            conditions.append("product_name LIKE ?")
            params.append(f"%{self.search_product.text()}%")
        if self.search_saler.text():
            conditions.append("saler_name LIKE ?")
            params.append(f"%{self.search_saler.text()}%")

        query = "SELECT * FROM sales"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(query,params)
        results = self.cursor.fetchall()

        self.table_widget.setRowCount(len(results))
        for row_idx,row_data in enumerate(results):
            for col_idx,value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                self.table_widget.setItem(row_idx,col_idx,item)

    def save_edit(self):
        try:
            self.cursor.execute('''
                                UPDATE sales
                                SET product_name = ?,
                                    saler_name   = ?,
                                    region       = ?,
                                    date         = ?,
                                    price        = ?
                                WHERE id = ?
                                ''',(
                                    self.edit_product.text(),
                                    self.edit_saler.text(),
                                    self.edit_region.text(),
                                    self.edit_date.text(),
                                    self.edit_price.value(),
                                    self.edit_id.text()
                                ))
            self.conn.commit()
            self.refresh_table()
            QMessageBox.information(self,"Успех","Запись обновлена")
        except Exception as e:
            QMessageBox.critical(self,"Ошибка",f"Ошибка обновления: {str(e)}")

    def delete_record(self):
        if not self.edit_id.text():
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены что хотите удалить запись?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM sales WHERE id = ?",(self.edit_id.text(),))
                self.conn.commit()
                self.refresh_table()
                self.clear_edit_form()
                QMessageBox.information(self,"Успех","Запись удалена")
            except Exception as e:
                QMessageBox.critical(self,"Ошибка",f"Ошибка удаления: {str(e)}")

    def clear_all_sales(self):
        reply = QMessageBox.question(
            self,
            "Очистка базы",
            "Вы уверены что хотите удалить все записи?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM sales")
                self.conn.commit()
                self.refresh_table()
                QMessageBox.information(self,"Успех","Все записи удалены")
            except Exception as e:
                QMessageBox.critical(self,"Ошибка",f"Ошибка очистки: {str(e)}")

    def export_to_excel(self):
        try:
            query = "SELECT * FROM sales"
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            df = pd.DataFrame(data,columns=["ID","Product Name","Saler Name","Region","Date","Price"])

            file_path,_ = QFileDialog.getSaveFileName(
                self,
                "Сохранить файл Excel",
                "",
                "Excel Files (*.xlsx)"
            )

            if file_path:
                df.to_excel(file_path,index=False)
                QMessageBox.information(self,"Успех","Данные успешно экспортированы в Excel")

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",f"Ошибка экспорта: {str(e)}")

    def import_from_excel(self):
        try:
            file_path,_ = QFileDialog.getOpenFileName(
                self,
                "Выберите файл Excel",
                "",
                "Excel Files (*.xlsx *.xls)"
            )

            if file_path:
                df = pd.read_excel(file_path)

                # Конвертация даты
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d.%m.%Y')

                # Вставка данных
                for _,row in df.iterrows():
                    self.cursor.execute('''
                                        INSERT INTO sales (product_name, saler_name, region, date, price)
                                        VALUES (?, ?, ?, ?, ?)
                                        ''',(
                                            row['Product Name'],
                                            row['Saler Name'],
                                            row['Region'],
                                            row['Date'],
                                            row['Price']
                                        ))

                self.conn.commit()
                self.refresh_table()
                QMessageBox.information(self,"Успех","Данные успешно импортированы")

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",f"Ошибка импорта: {str(e)}")

    def clear_add_form(self):
        self.add_product_name.clear()
        self.add_saler_name.clear()
        self.add_region.clear()
        self.add_date.setDateTime(QDateTime.currentDateTime())
        self.add_price.setValue(0.0)

    def clear_search_form(self):
        self.search_id.clear()
        self.search_product.clear()
        self.search_saler.clear()
        self.refresh_table()

    def clear_edit_form(self):
        self.edit_id.clear()
        self.edit_product.clear()
        self.edit_saler.clear()
        self.edit_region.clear()
        self.edit_date.setDateTime(QDateTime.currentDateTime())
        self.edit_price.setValue(0.0)

    def go_back(self):
        self.previous_window.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SalesManagementWindow(None, None, "admin")
    window.show()
    sys.exit(app.exec_())