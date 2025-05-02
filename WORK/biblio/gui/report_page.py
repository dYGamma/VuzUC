from PyQt5 import QtWidgets
import controllers

class ReportPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        btn_pdf = QtWidgets.QPushButton("PDF — низкий остаток")
        btn_excel = QtWidgets.QPushButton("Excel — просроченные")
        btn_pdf.clicked.connect(self._pdf)
        btn_excel.clicked.connect(self._excel)
        layout.addWidget(btn_pdf)
        layout.addWidget(btn_excel)

    def _pdf(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить PDF", "", "PDF (*.pdf)"
        )
        if path:
            controllers.export_low_stock_pdf(path)

    def _excel(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить XLSX", "", "Excel (*.xlsx)"
        )
        if path:
            controllers.export_overdue_excel(path)
