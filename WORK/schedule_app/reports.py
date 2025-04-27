# reports.py

import os
from datetime import date
from reportlab.platypus import SimpleDocTemplate, LongTable, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from openpyxl import Workbook
from db import SessionLocal
from models import Schedule, Homework

# Регистрация кириллического шрифта
FONT_PATH = None
for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/DejaVuSans.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
]:
    if os.path.exists(p):
        FONT_PATH = p
        break

if FONT_PATH:
    pdfmetrics.registerFont(TTFont("MyFont", FONT_PATH))
    BASE_FONT = "MyFont"
else:
    BASE_FONT = "Helvetica"
    print("[reports] WARNING: Cyrillic font not found, using Helvetica")


def export_pdf(path):
    db = SessionLocal()
    try:
        # стили
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="MyHeading1",
            parent=styles["Heading1"],
            fontName=BASE_FONT,
            fontSize=18,
            leading=22,
            spaceAfter=12
        ))
        styles.add(ParagraphStyle(
            name="MyNormal",
            parent=styles["Normal"],
            fontName=BASE_FONT,
            fontSize=10,
            leading=12,
            wordWrap="LTR"
        ))

        # документ с отступами
        doc = SimpleDocTemplate(
            path,
            pagesize=A4,
            leftMargin=36, rightMargin=36,
            topMargin=36, bottomMargin=36
        )
        elems = []

        # доступная ширина
        page_width, _ = A4
        avail_width = page_width - doc.leftMargin - doc.rightMargin

        # общий стиль таблицы
        table_style = [
            ("FONTNAME",   (0, 0), (-1, -1), BASE_FONT),
            ("FONTSIZE",   (0, 0), (-1, -1), 10),
            ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ]

        # === Отчёт по расписанию ===
        elems.append(Paragraph("Отчёт по расписанию", styles["MyHeading1"]))
        elems.append(Spacer(1, 12))

        lessons = db.query(Schedule).order_by(Schedule.date, Schedule.start_time).all()
        data = [[
            Paragraph(h, styles["MyNormal"]) for h in
            ["ID","Дата","Предмет","Преподаватель","Начало","Конец","Кабинет","Тип"]
        ]]
        for l in lessons:
            data.append([
                Paragraph(str(l.id), styles["MyNormal"]),
                Paragraph(l.date.isoformat(), styles["MyNormal"]),
                Paragraph(l.subject, styles["MyNormal"]),
                Paragraph(l.teacher, styles["MyNormal"]),
                Paragraph(l.start_time.strftime("%H:%M"), styles["MyNormal"]),
                Paragraph(l.end_time.strftime("%H:%M"), styles["MyNormal"]),
                Paragraph(l.room or "", styles["MyNormal"]),
                Paragraph(l.type, styles["MyNormal"]),
            ])

        # задаём ширины колонок так, чтобы сумма ≈ avail_width
        col_widths = [
            30,    # ID
            60,    # Дата
            100,   # Предмет
            90,    # Преподаватель
            50,    # Начало
            50,    # Конец
            50,    # Кабинет
            avail_width - (30 + 60 + 100 + 90 + 50 + 50 + 50)
        ]

        tbl = LongTable(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(table_style)
        elems.append(tbl)
        elems.append(Spacer(1, 24))

        # === Отчёт по домашним заданиям ===
        elems.append(Paragraph("Отчёт по домашним заданиям", styles["MyHeading1"]))
        elems.append(Spacer(1, 12))

        hws = db.query(Homework).order_by(Homework.due_date).all()
        data2 = [[
            Paragraph(h, styles["MyNormal"]) for h in
            ["ID","Заголовок","Описание","Срок","Состояние","Файл"]
        ]]
        today = date.today()
        for hw in hws:
            status = "Завершено" if hw.due_date and hw.due_date < today else "В процессе"
            data2.append([
                Paragraph(str(hw.id), styles["MyNormal"]),
                Paragraph(hw.title, styles["MyNormal"]),
                Paragraph(hw.description or "", styles["MyNormal"]),
                Paragraph(hw.due_date.isoformat() if hw.due_date else "", styles["MyNormal"]),
                Paragraph(status, styles["MyNormal"]),
                Paragraph(os.path.basename(hw.attachment or ""), styles["MyNormal"]),
            ])

        # вычисляем ширины для 6 колонок
        fixed = 30 + 80 + 60 + 50 + 50  # ID, Заголовок, Срок, Статус, Файл
        col_widths2 = [
            30,   # ID
            80,   # Заголовок
            avail_width - fixed,  # Описание
            60,   # Срок
            50,   # Состояние
            50    # Файл
        ]

        tbl2 = LongTable(data2, colWidths=col_widths2, repeatRows=1, hAlign="LEFT")
        tbl2.setStyle(table_style)
        elems.append(tbl2)

        # финальный рендеринг
        doc.build(elems)

    finally:
        db.close()
        SessionLocal.remove()


def export_excel(path):
    db = SessionLocal()
    try:
        wb = Workbook()
        # Расписание
        ws1 = wb.active
        ws1.title = "Расписание"
        ws1.append(["ID","Дата","Предмет","Преподаватель","Начало","Конец","Кабинет","Тип занятия"])
        for l in db.query(Schedule).order_by(Schedule.date, Schedule.start_time).all():
            ws1.append([
                l.id,
                l.date.isoformat(),
                l.subject,
                l.teacher,
                l.start_time.strftime("%H:%M"),
                l.end_time.strftime("%H:%M"),
                l.room or "",
                l.type
            ])

        # Домашние задания
        ws2 = wb.create_sheet("Домашние задания")
        ws2.append(["ID","Заголовок","Описание","Срок","Состояние","Файл"])
        today = date.today()
        for hw in db.query(Homework).order_by(Homework.due_date).all():
            status = "Завершено" if hw.due_date and hw.due_date < today else "В процессе"
            ws2.append([
                hw.id,
                hw.title,
                hw.description or "",
                hw.due_date.isoformat() if hw.due_date else "",
                status,
                os.path.basename(hw.attachment or "")
            ])

        wb.save(path)
    finally:
        db.close()
        SessionLocal.remove()
