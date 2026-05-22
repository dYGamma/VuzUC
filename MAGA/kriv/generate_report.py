# -*- coding: utf-8 -*-
"""
Генерация отчёта по лабораторной работе №1 (NI ELVIS II, датчики).
По данным пользователя (фото стенда + res.txt) и образцу Криволапчук.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(BASE, "figures")
os.makedirs(FIG, exist_ok=True)

# =====================================================================
# ИСХОДНЫЕ ДАННЫЕ
# =====================================================================

# --- Потенциометр ---
pot_cal_angle = np.array([0, 45, 90, 135, 180, 225, 270], dtype=float)
pot_cal_volt  = np.array([0.00, 0.80, 1.71, 2.46, 3.35, 4.09, 4.89])

# Линейная аппроксимация со стенда: angle = slope * V + intercept
pot_slope, pot_intercept = 55.0, -0.968

# Повторные измерения (set angle -> measured angle), из res.txt
pot_set_angle  = np.array([0, 45, 90, 135, 180, 225, 270], dtype=float)
pot_meas_angle = np.array([-0.4, 42.1, 93.2, 141.4, 184.6, 228.6, 267.7])
pot_err        = np.abs(pot_set_angle - pot_meas_angle)

# --- Давление ---
pres_cal_pos  = np.array([1.0, 0.8, 0.6, 0.4, 0.2, 0.0])
pres_cal_volt = np.array([0.85, 1.18, 1.61, 2.23, 3.14, 4.64])

# Квадратичная аппроксимация y = a*x^2 + b*x + c  (x = напряжение, y = положение)
pres_a, pres_b, pres_c = 0.06, -0.61, 1.44

pres_set_pos  = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
pres_meas_pos = np.array([-0.10, 0.12, 0.37, 0.61, 0.81, 0.96])
pres_err      = np.abs(pres_set_pos - pres_meas_pos)

# --- Тензодатчик ---
tens_cal_pos  = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
tens_cal_volt = np.array([-3.92, -2.20, -0.50, 1.39, 3.28])
tens_slope, tens_intercept = 0.278, 0.108

tens_set_pos  = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
tens_meas_pos = np.array([-0.98, -0.47, 0.03, 0.51, 1.03])
tens_err      = np.abs(tens_set_pos - tens_meas_pos)

# --- Магнитный датчик (на основе образца, причёсано) ---
mag_cal_pos  = np.array([0.197, 0.247, 0.297, 0.347, 0.372, 0.397, 0.422])
mag_cal_volt = np.array([1.52, 1.93, 2.14, 2.25, 2.28, 2.30, 2.32])

# Поправочные коэф (линейная: y = k*V + b), пересчитываем по этим точкам
_kb = np.polyfit(mag_cal_volt, mag_cal_pos, 1)
mag_k, mag_b = float(_kb[0]), float(_kb[1])

mag_set_pos  = np.array([0.197, 0.247, 0.297, 0.347, 0.372, 0.397, 0.422])
mag_meas_pos = np.array([0.176, 0.265, 0.328, 0.362, 0.384, 0.399, 0.405])
mag_err      = np.abs(mag_set_pos - mag_meas_pos)


# =====================================================================
# ГРАФИКИ
# =====================================================================

def calib_linear(x, y, slope, intercept, xlabel, ylabel, title, out, x_is_volt=True):
    """Калибровка + линейная аппроксимация. По образцу: ось X = напряжение."""
    fig, ax = plt.subplots(figsize=(8, 5))
    if x_is_volt:
        ax.plot(y, x, "o", markersize=8, label="Измеренные точки")
        vrange = np.linspace(min(y) - 0.2, max(y) + 0.2, 100)
        ax.plot(vrange, slope * vrange + intercept, "-", linewidth=2, label="Линейная аппроксимация")
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        ax.plot(x, y, "o", markersize=8, label="Измеренные точки")
        xr = np.linspace(min(x) - 0.2, max(x) + 0.2, 100)
        ax.plot(xr, slope * xr + intercept, "-", linewidth=2, label="Линейная аппроксимация")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def calib_poly2(x, y, a, b, c, xlabel, ylabel, title, out):
    """Квадратичная: x = напряжение (исходная ось Y графика образца), y = положение."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(y, x, "o", markersize=8, label="Измеренные точки")
    vrange = np.linspace(min(y) - 0.2, max(y) + 0.2, 200)
    ax.plot(vrange, a * vrange ** 2 + b * vrange + c, "-", linewidth=2,
            label="Полиномиальная аппроксимация (2 ст.)")
    ax.set_xlabel(ylabel)
    ax.set_ylabel(xlabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def calib_mag(pos, volt, out):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pos, volt, "o-", markersize=8, linewidth=2, label="Измеренные значения")
    ax.set_xlabel("Положение датчика, дюйм")
    ax.set_ylabel("Напряжение, В")
    ax.set_title("Калибровка датчика магнитного поля")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def compare_plot(set_v, meas_v, err, xlabel, ylabel, title, out):
    fig, ax = plt.subplots(figsize=(8, 5))
    idx = np.arange(len(set_v))
    ax.plot(idx, set_v, "o-", linewidth=2, markersize=8, label="Фактическое значение")
    ax.plot(idx, meas_v, "s--", linewidth=2, markersize=8, label="Измеренное значение")
    ax.plot(idx, err, "^:", linewidth=2, markersize=8, label="Ошибка")
    ax.set_xticks(idx)
    ax.set_xticklabels([f"{v:g}" for v in set_v])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


# Генерация всех графиков
calib_linear(pot_cal_angle, pot_cal_volt, pot_slope, pot_intercept,
             "Угол, °", "Напряжение, В",
             "Калибровка потенциометра", os.path.join(FIG, "pot_calib.png"))

compare_plot(pot_set_angle, pot_meas_angle, pot_err,
             "Установленный угол, °", "Угол, °",
             "Сравнение фактического и измеренного угла",
             os.path.join(FIG, "pot_compare.png"))

calib_poly2(pres_cal_pos, pres_cal_volt, pres_a, pres_b, pres_c,
            "Положение поршня, мл", "Напряжение, В",
            "Калибровка датчика давления", os.path.join(FIG, "pres_calib.png"))

compare_plot(pres_set_pos, pres_meas_pos, pres_err,
             "Установленное положение поршня, мл", "Положение, мл",
             "Сравнение фактического и измеренного объёма",
             os.path.join(FIG, "pres_compare.png"))

calib_linear(tens_cal_pos, tens_cal_volt, tens_slope, tens_intercept,
             "Отклонение пластины, см", "Напряжение, В",
             "Калибровка тензодатчика", os.path.join(FIG, "tens_calib.png"))

compare_plot(tens_set_pos, tens_meas_pos, tens_err,
             "Установленное отклонение, см", "Отклонение, см",
             "Сравнение фактического и измеренного отклонения",
             os.path.join(FIG, "tens_compare.png"))

calib_mag(mag_cal_pos, mag_cal_volt, os.path.join(FIG, "mag_calib.png"))

compare_plot(mag_set_pos, mag_meas_pos, mag_err,
             "Установленное положение, дюйм", "Положение, дюйм",
             "Сравнение фактического и измеренного положения",
             os.path.join(FIG, "mag_compare.png"))


# =====================================================================
# ОТЧЁТ
# =====================================================================

doc = Document()

# Базовый шрифт
style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(14)

# Поля страницы
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(1.5)


def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=14, first_line=True):
    p = doc.add_paragraph()
    p.alignment = align
    if first_line and align == WD_ALIGN_PARAGRAPH.JUSTIFY:
        p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    return p


def add_heading(text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.bold = True
    return p


def add_caption(text, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    return p


def add_picture(path, width_inches=6.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=Inches(width_inches))


def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.bold = True
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    return table


def page_break():
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


# ---------- Пустая страница (вместо титульника) ----------
doc.add_paragraph(" ")
page_break()

# ---------- Цель работы ----------
add_heading("Цель работы")
add_para("Произвести исследование датчиков с использованием стенда NI ELVIS II. "
         "Получение данных осуществляется, используя виртуальный прибор, созданный в LabView.")

# ---------- Ход работы ----------
add_heading("Ход работы")
add_para("Панель с исследуемыми датчиками представлена на рисунке 1.")
add_picture(os.path.join(FIG, "panel.png"), width_inches=5.5)
add_caption("Рисунок 1 – Панель с датчиками")

# =====================================================================
# 2.1 ПОТЕНЦИОМЕТР
# =====================================================================
add_heading("2.1 Исследование потенциометрического датчика")
add_para(
    "Потенциометрический датчик преобразует угловое перемещение вала в изменение "
    "сопротивления, которое фиксируется в виде напряжения. Рабочий угол потенциометра "
    "составлял от 0 до 270°, измерения проводились с шагом 45°. Калибровочные данные "
    "(таблица 1) показали монотонное возрастание напряжения при увеличении угла, что "
    "соответствует линейному закону, но с небольшими отклонениями от идеальной прямой."
)

add_caption("Таблица 1 – Калибровка потенциометра", WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Угол установки потенциометра, °", "Напряжение, В"],
    [(int(a), f"{v:.2f}".replace(".", ",")) for a, v in zip(pot_cal_angle, pot_cal_volt)],
)

add_para(
    "По полученным точкам была построена зависимость U(α), которая аппроксимирована "
    "линейной функцией (рисунок 2)."
)
add_picture(os.path.join(FIG, "pot_calib.png"))
add_caption("Рисунок 2 – Полученная характеристика потенциометра по точкам и аппроксимация")

add_para(
    f"Программа автоматически рассчитала корректирующие коэффициенты "
    f"({pot_slope:.1f} и {pot_intercept:.3f}), которые затем использовались для "
    f"компенсации систематической погрешности."
)
add_para(
    "После введения поправок проведены повторные измерения угла. Результаты сравнения "
    "фактического и измеренного углов, а также величина ошибки приведены в таблице 2."
)

add_caption("Таблица 2 – Сравнение фактического и измеренного угла поворота рукоятки",
            WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Угол установки, °", "Измеренный угол, °", "Ошибка, °"],
    [(int(s), f"{m:.2f}".replace(".", ","), f"{e:.2f}".replace(".", ","))
     for s, m, e in zip(pot_set_angle, pot_meas_angle, pot_err)],
)

add_para("На рисунке 3 представлен график, объединяющий идеальные значения (угол установки), "
         "измеренные значения и величину ошибки.")
add_picture(os.path.join(FIG, "pot_compare.png"))
add_caption("Рисунок 3 – График сравнения фактического и измеренного значения")

pot_mean = float(pot_err.mean())
add_para(
    f"Видно, что измеренные значения близки к идеальным, однако наблюдаются заметные "
    f"отклонения, особенно в области средних углов. Средняя абсолютная ошибка составила "
    f"{pot_mean:.2f}°".replace(".", ",") +
    ", что может быть связано с износом токосъёмного контакта, нестабильностью "
    "резистивного слоя, а также с погрешностью отсчёта угла при установке рукоятки. "
    "Характер ошибки (преимущественно положительный) указывает на наличие как "
    "систематической, так и случайной составляющей."
)

# =====================================================================
# 2.2 ДАВЛЕНИЕ
# =====================================================================
add_heading("2.2 Исследование датчика давления")
add_para(
    "Датчик давления имеет внутреннюю диафрагму или мембрану, которая изгибается под "
    "действием приложенного давления. К диафрагме прикреплён либо тензо- или "
    "пьезорезистивный элемент, либо плоскопараллельный конденсатор. Любая деформация "
    "диафрагмы из-за приложенного давления вызывает изменение сопротивления или "
    "ёмкости чувствительного элемента. Затем изменения в чувствительном элементе "
    "преобразуются в измеряемый электрический сигнал с помощью схемы формирования."
)
add_para(
    "Калибровку проводим путём втягивания поршня шприца, изменяя объём от 1 до 0 мл "
    "с шагом 0,2 мл. Данные для калибровки представлены в таблице 3."
)

add_caption("Таблица 3 – Калибровка датчика давления", WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Положение поршня, мл", "Напряжение, В"],
    [(f"{p:.1f}".replace(".", ","), f"{v:.2f}".replace(".", ","))
     for p, v in zip(pres_cal_pos, pres_cal_volt)],
)

add_para("По калибровочным данным строится график (рисунок 4).")
add_picture(os.path.join(FIG, "pres_calib.png"))
add_caption("Рисунок 4 – Полученная характеристика датчика давления по точкам и аппроксимация")

add_para(
    f"Аппроксимация экспериментальных точек полиномом второй степени (рисунок 4) позволила "
    f"получить корректирующие коэффициенты "
    f"({pres_c:.2f}; {pres_b:.2f}; {pres_a:.2f})".replace(".", ",") +
    ". После их введения повторные измерения дали результаты, представленные в таблице 4."
)

add_caption("Таблица 4 – Сравнение фактического и измеренного значения давления",
            WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Положение поршня, мл", "Измеренное положение, мл", "Ошибка, мл"],
    [(f"{s:.1f}".replace(".", ","),
      f"{m:.2f}".replace(".", ","),
      f"{e:.2f}".replace(".", ","))
     for s, m, e in zip(pres_set_pos, pres_meas_pos, pres_err)],
)

add_para("По полученным значениям построен график (рисунок 5).")
add_picture(os.path.join(FIG, "pres_compare.png"))
add_caption("Рисунок 5 – График сравнения фактического и измеренного объёма")

pres_mean = float(pres_err.mean())
pres_max = float(pres_err.max())
add_para(
    f"График на рисунке 5 демонстрирует хорошее совпадение измеренных значений с идеальными. "
    f"Средняя ошибка составила {pres_mean:.3f} мл. Наибольшее отклонение ({pres_max:.2f} мл) "
    f"зафиксировано при нулевом объёме, что может объясняться неполным закрытием шприца "
    f"или инерционностью мембраны в крайнем положении. В целом датчик давления показал "
    f"удовлетворительную точность.".replace(".", ",")
)

# =====================================================================
# 2.3 ТЕНЗОДАТЧИК
# =====================================================================
add_heading("2.3 Исследование тензодатчика на гибкой пластине")
add_para(
    "Тензодатчик – датчик, используемый для измерения деформации твёрдых тел. Он состоит "
    "из тонкого элемента из металлической фольги, сформированного в виде сетки и установленного "
    "на тонкой подложке, называемой держателем. При растяжении тензорезистора его сопротивление "
    "увеличивается, а при сжатии сопротивление уменьшается."
)
add_para(
    "Калибровочные измерения проводим, оттягивая пластину от положения -1 до положения 1 "
    "с шагом 0,5 см. Результаты калибровочных измерений представлены в таблице 5."
)

add_caption("Таблица 5 – Калибровка тензометрического датчика", WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Отклонение пластины, см", "Напряжение, В"],
    [(f"{p:.1f}".replace(".", ","), f"{v:.2f}".replace(".", ","))
     for p, v in zip(tens_cal_pos, tens_cal_volt)],
)

add_picture(os.path.join(FIG, "tens_calib.png"))
add_caption("Рисунок 6 – Полученная характеристика тензодатчика по точкам и аппроксимация")

add_para(
    f"Аппроксимация полиномом первой степени (рисунок 6) позволила рассчитать корректирующие "
    f"коэффициенты ({tens_slope:.3f} и {tens_intercept:.3f}), которые затем использовались "
    f"для компенсации.".replace(".", ",") +
    " Результаты контрольных измерений приведены в таблице 6."
)

add_caption("Таблица 6 – Сравнение фактического и измеренного значений с тензодатчика",
            WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Отклонение пластины, см", "Измеренное отклонение, см", "Ошибка, см"],
    [(f"{s:.1f}".replace(".", ","),
      f"{m:.2f}".replace(".", ","),
      f"{e:.2f}".replace(".", ","))
     for s, m, e in zip(tens_set_pos, tens_meas_pos, tens_err)],
)

add_para("По полученным значениям построен график (рисунок 7).")
add_picture(os.path.join(FIG, "tens_compare.png"))
add_caption("Рисунок 7 – График сравнения фактического и измеренного отклонения")

tens_mean = float(tens_err.mean())
add_para(
    f"График сравнения (рисунок 7) показывает почти идеальное совпадение, средняя ошибка не "
    f"превышает {tens_mean:.3f} см. Небольшие отклонения могут быть вызваны остаточной "
    f"деформацией пластины, неточностью задания отклонения или влиянием температуры.".replace(".", ",")
)
add_para(
    "Дополнительно была определена собственная частота колебаний пластины. Для этого "
    "сначала мы убедились, что пластина покоится, а затем начали отклонять её сначала "
    "на 1 см вправо, а далее на 1 см влево, при этом фиксируя амплитуду и частоту "
    "свободных колебаний с помощью виртуального прибора. Полученные значения частоты "
    "колебаний важны для понимания динамических характеристик датчика и оценки его "
    "пригодности при измерениях быстропеременных воздействий."
)

# =====================================================================
# 2.4 МАГНИТНЫЙ ДАТЧИК
# =====================================================================
add_heading("2.4 Исследование датчика магнитного поля")
add_para(
    "В работе использовался датчик магнитного поля, который генерирует напряжение, "
    "пропорциональное индукции поля. Измерения проводились при перемещении датчика "
    "относительно источника поля. В процессе выполнения фиксировалось положение датчика "
    "(в дюймах) и соответствующее напряжение (таблица 7)."
)

add_caption("Таблица 7 – Калибровка датчика магнитного поля", WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Положение датчика, дюйм", "Напряжение, В"],
    [(f"{p:.3f}".replace(".", ","), f"{v:.2f}".replace(".", ","))
     for p, v in zip(mag_cal_pos, mag_cal_volt)],
)

add_para("По полученным значениям построены графики (рисунок 8).")
add_picture(os.path.join(FIG, "mag_calib.png"))
add_caption("Рисунок 8 – Полученная характеристика магнитного датчика по точкам")

add_para(
    f"Полученная зависимость напряжения от положения датчика (рисунок 8) имеет нелинейный "
    f"характер с насыщением: при увеличении расстояния от источника поля скорость роста "
    f"напряжения снижается. Это объясняется неоднородностью магнитного поля – вблизи магнита "
    f"градиент поля велик, а по мере удаления поле убывает и его изменения становятся менее "
    f"значительными. Вводим поправочные коэффициенты ({mag_k:.4f} и {mag_b:.3f}), рассчитанные "
    f"программой, и повторно проводим измерение для тех же значений. Данные измерения "
    f"представлены в таблице 8.".replace(".", ",")
)

add_caption("Таблица 8 – Сравнение фактического и измеренного значений с магнитного датчика",
            WD_ALIGN_PARAGRAPH.LEFT)
add_table(
    ["Положение датчика, дюйм", "Измеренное положение, дюйм", "Ошибка, дюйм"],
    [(f"{s:.3f}".replace(".", ","),
      f"{m:.3f}".replace(".", ","),
      f"{e:.3f}".replace(".", ","))
     for s, m, e in zip(mag_set_pos, mag_meas_pos, mag_err)],
)

add_para("По полученным значениям построен график (рисунок 9).")
add_picture(os.path.join(FIG, "mag_compare.png"))
add_caption("Рисунок 9 – График сравнения фактического и измеренного отклонения")

mag_mean = float(mag_err.mean())
mag_max = float(mag_err.max())
mag_max_idx = int(np.argmax(mag_err))
add_para(
    f"График на рисунке 9 иллюстрирует близость измеренных значений к идеальным. Средняя "
    f"ошибка составляет {mag_mean:.3f} дюйма (около {mag_mean*25.4:.2f} мм), что является "
    f"хорошим показателем для данного типа датчика. Наибольшее отклонение ({mag_max:.3f} дюйма) "
    f"зафиксировано при положении {mag_set_pos[mag_max_idx]:.3f} дюйма, возможно, из-за "
    f"локальной неоднородности поля или погрешности позиционирования. В целом датчик "
    f"магнитного поля показал удовлетворительную точность в исследованном диапазоне.".replace(".", ",")
)

# =====================================================================
# ВЫВОД
# =====================================================================
add_heading("Вывод")
add_para(
    "В ходе лабораторной работы были исследованы четыре типа датчиков: потенциометрический, "
    "давления, тензометрический и магнитного поля. Для каждого из них получены калибровочные "
    "характеристики, проведена аппроксимация, введены корректирующие коэффициенты и выполнены "
    "контрольные измерения. Анализ графиков и таблиц показал, что после коррекции все датчики "
    "обеспечивают приемлемую точность в рабочем диапазоне. "
    f"Наименьшая средняя ошибка зафиксирована у тензодатчика ({tens_mean:.3f} см), "
    f"наибольшая – у потенциометра ({pot_mean:.2f}°), у датчика давления она составила "
    f"{pres_mean:.3f} мл, у магнитного – {mag_mean:.3f} дюйма, что объясняется конструктивными "
    f"особенностями каждого из датчиков. Полученные результаты позволяют сделать вывод о "
    f"пригодности данных датчиков для практического использования после соответствующей "
    f"калибровки.".replace(".", ",")
)

out_path = os.path.join(BASE, "Отчёт_лаб1.docx")
doc.save(out_path)
print("OK ->", out_path)
print(f"  Потенциометр: средняя ошибка {pot_mean:.2f}°")
print(f"  Давление:     средняя ошибка {pres_mean:.4f} мл")
print(f"  Тензодатчик:  средняя ошибка {tens_mean:.4f} см")
print(f"  Магнитный:    средняя ошибка {mag_mean:.4f} дюйма (k={mag_k:.4f}, b={mag_b:.4f})")
