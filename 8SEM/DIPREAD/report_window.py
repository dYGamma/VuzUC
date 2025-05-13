import openpyxl
import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,
                             QPushButton,QTableWidget,QTableWidgetItem,QGroupBox,
                             QFormLayout,QFileDialog,QRadioButton,QHeaderView)
from PyQt5.QtCore import Qt,QFileInfo
from PyQt5.QtGui import QTextDocumentWriter
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


class ReportAnalysisWindow(QWidget):
    def __init__(self,previous_window,login_window,username):
        super().__init__()

        self.setWindowTitle("Анализ продаж")
        self.showFullScreen()

        self.previous_window = previous_window
        self.login_window = login_window
        self.username = username
        self.init_ui()
        self.init_db()
        self.populate_sales_table()

    def setFullScreen(self):
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
        self.setGeometry(screen_geometry)

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

    def init_ui(self):
        # Top GroupBox
        top_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        window_name_label = QLabel("Анализ продаж")
        username_label = QLabel(f"Username: {self.username}")

        top_layout.addWidget(back_button)
        top_layout.addStretch()
        top_layout.addWidget(window_name_label)
        top_layout.addStretch()
        top_layout.addWidget(username_label)

        top_groupbox = QGroupBox()
        top_groupbox.setLayout(top_layout)

        # Main content area
        main_layout = QHBoxLayout()

        # Left side - Table
        left_layout = QVBoxLayout()
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(6)
        self.sales_table.setHorizontalHeaderLabels(["ID","Product Name","Saler Name","Region","Date","Price"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sales_table.verticalHeader().setVisible(False)

        left_layout.addWidget(self.sales_table)
        left_groupbox = QGroupBox("Таблица продаж")
        left_groupbox.setLayout(left_layout)

        # Right side - Controls
        right_layout = QVBoxLayout()
        right_groupbox = QGroupBox("Анализ и отчеты")

        # Report format selection
        format_layout = QVBoxLayout()
        self.radio_img = QRadioButton("График (PNG)")
        self.radio_excel = QRadioButton("Excel отчет")
        self.radio_excel.setChecked(True)

        format_layout.addWidget(QLabel("Формат отчета:"))
        format_layout.addWidget(self.radio_img)
        format_layout.addWidget(self.radio_excel)

        # Buttons
        button_layout = QVBoxLayout()
        self.save_button = QPushButton("Скачать отчет")
        button_layout.addStretch()
        button_layout.addLayout(format_layout)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()

        right_groupbox.setLayout(button_layout)

        # Add to main layout
        main_layout.addWidget(left_groupbox,75)  # 75% width
        main_layout.addWidget(right_groupbox,25)  # 25% width

        # Overall layout
        overall_layout = QVBoxLayout()
        overall_layout.addWidget(top_groupbox)
        overall_layout.addLayout(main_layout)

        self.setLayout(overall_layout)

        # Signals
        back_button.clicked.connect(self.go_back)
        self.save_button.clicked.connect(self.save_report)

    def go_back(self):
        self.previous_window.show()
        self.hide()

    def save_report(self):
        # Get the selected report format
        if self.radio_img.isChecked():
            file_extension = "png"
        elif self.radio_excel.isChecked():
            file_extension = "xlsx"
        else:
            return  # No format selected

        # Open a file dialog to choose the file path and name
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", f"{file_extension.upper()} files (*.{file_extension})")
        print(file_path)
        if file_path:
            # Check if the file already exists
            file_info = QFileInfo(file_path)
            if file_info.exists():
                return  # File already exists

            # Get the data from the table
            num_rows = self.sales_table.rowCount()
            num_cols = self.sales_table.columnCount()

            data = []
            for row in range(num_rows):
                row_data = []
                for col in range(num_cols):
                    item = self.sales_table.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)

            # Convert the data to a DataFrame
            df = pd.DataFrame(data, columns=["ID", "Product Name", "Saler Name", "Region", "Date", "Price"])

            # Perform sales analysis
            df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

            # Count occurrences of each product
            product_counts = df["Product Name"].value_counts()

            # Calculate average occurrences
            average_occurrences = product_counts.mean()

            # Apply conditional formatting to highlight occurrences below and above the average
            df_style = df.style.apply(lambda x: ['background-color: red' if product_counts.get(x['Product Name'], 0) < average_occurrences else 'background-color: green' if product_counts.get(x['Product Name'], 0) > average_occurrences else '' for i in x], axis=1)

            # Save the styled DataFrame to a file based on the selected format
            if file_extension == "png":

                df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

                product_counts.plot(kind='bar')

                plt.xlabel("Product Name")
                plt.ylabel("Total Sales")
                plt.title("Total Sales per Product")
                plt.tight_layout()

                # Save the plot to a temporary file
                temp_plot_file = file_path
                print(temp_plot_file)
                plt.savefig(temp_plot_file)
                plt.close()

            elif file_extension == "xlsx":
                # Save the DataFrame to an Excel file
                df_style.to_excel(file_path, index=False)

                # Additional code to save product sales plot to the same Excel file
                # Assuming you have the necessary imports and setup for plotting

                product_sales = df.groupby("Product Name")["Price"].sum().reset_index()

                # Save the DataFrame and the plot to the report file
                with pd.ExcelWriter(file_path, mode="a", engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sales Data")
                    product_sales.to_excel(writer, index=False, sheet_name="Product Sales")

    # def save_report(self):
    #     # Get the selected report format
    #     if self.radio_pdf.isChecked():
    #         file_extension = "pdf"
    #     elif self.radio_excel.isChecked():
    #         file_extension = "xlsx"
    #     else:
    #         return  # No format selected

    #     # Open a file dialog to choose the file path and name
    #     file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", f"{file_extension.upper()} files (*.{file_extension})")

    #     if file_path:
    #         # Check if the file already exists
    #         file_info = QFileInfo(file_path)
    #         if file_info.exists():
    #             return  # File already exists

    #         # Get the data from the table
    #         num_rows = self.sales_table.rowCount()
    #         num_cols = self.sales_table.columnCount()

    #         data = []
    #         for row in range(num_rows):
    #             row_data = []
    #             for col in range(num_cols):
    #                 item = self.sales_table.item(row, col)
    #                 if item:
    #                     row_data.append(item.text())
    #                 else:
    #                     row_data.append("")
    #             data.append(row_data)

    #         # Convert the data to a DataFrame
    #         df = pd.DataFrame(data, columns=["ID", "Product Name", "Saler Name", "Region", "Date", "Price"])

    #         # Save the DataFrame to a file based on the selected format
    #         if file_extension == "pdf":
    #             writer = QTextDocumentWriter(file_path)
    #             writer.setFormat("pdf")
    #             writer.write(df.to_html())
    #         elif file_extension == "xlsx":
    #             df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    #             product_sales = df.groupby("Product Name")["Price"].sum().reset_index()

    #             # Example: Plot bar chart for product sales
                
                
    #             product_sales.plot(kind="bar", x="Product Name", y="Price", rot=45)
    #             plt.xlabel("Product Name")
    #             plt.ylabel("Total Sales")
    #             plt.title("Total Sales per Product")
    #             plt.tight_layout()

    #             # Save the plot to a temporary file
    #             temp_plot_file = "temp_plot.png"
    #             plt.savefig(temp_plot_file)
    #             plt.close()

    #             # Save the DataFrame and the plot to the report file
    #             with pd.ExcelWriter(file_path) as writer:
    #                 df.to_excel(writer, index=False, sheet_name="Sales Data")
    #                 product_sales.to_excel(writer, index=False, sheet_name="Product Sales")

    def populate_sales_table(self):
        query = "SELECT * FROM sales"
        self.cursor.execute(query)
        sales_data = self.cursor.fetchall()

        self.sales_table.setRowCount(len(sales_data))
        for row, sale in enumerate(sales_data):
            for col, value in enumerate(sale):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                self.sales_table.setItem(row, col, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportAnalysisWindow(None, None, "admin")
    window.show()
    sys.exit(app.exec_())