"""
Генерация отчёт_пр3.pdf
Стр.1-3: текст (А4), Стр.4-9: чертёж+спец×3 (А2+А4)
"""

import pymupdf, os, textwrap

BASE  = r'C:\VuzUC\MAGA\Nstya_SECOND'
FONTR_FILE = r'C:\Windows\Fonts\times.ttf'
FONTB_FILE = r'C:\Windows\Fonts\timesbd.ttf'
FONTR = 'TimesNewRoman'
FONTB = 'TimesNewRomanBold'
FS    = 14
LH    = FS * 1.5

A4W, A4H = 595, 842
ML = 85; MR = 43; MT = 57; MB = 57
TW = A4W - ML - MR          # ~467 pt

# Chars per line: empirical for Times 14pt in 467pt width
# ~72 chars for normal text, ~68 for indented (28pt indent)
CPL_FULL   = 72
CPL_INDENT = 68
CPL_BULLET = 65  # bullet text area (TW - 42pt)

def count_lines(text, cpl):
    """Estimate number of lines needed."""
    wrapped = textwrap.wrap(text, width=cpl)
    return max(len(wrapped), 1)

def draw_para(page, text, y, indent=True, cpl=None):
    if cpl is None:
        cpl = CPL_INDENT if indent else CPL_FULL
    x0 = ML + (28 if indent else 0)
    w  = TW - (28 if indent else 0)
    rc = pymupdf.Rect(x0, y, ML + TW, A4H - MB - 5)
    if rc.height < FS:
        return y  # no space
    page.insert_textbox(rc, text,
                        fontname=FONTR, fontsize=FS,
                        lineheight=1.5,
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    n = count_lines(text, cpl)
    return y + n * LH

def draw_bold(page, text, y, indent=True):
    x0 = ML + (28 if indent else 0)
    page.insert_text((x0, y + FS), text, fontname=FONTB, fontsize=FS)
    return y + LH

def draw_bold_para(page, bold_part, rest, y, indent=True):
    """Bold prefix on first line, then normal text continuation."""
    x0 = ML + (28 if indent else 0)
    # write bold word
    page.insert_text((x0, y + FS), bold_part, fontname=FONTB, fontsize=FS)
    # estimate bold width ≈ 0.58 * FS * chars (Times Bold)
    bw = 0.58 * FS * len(bold_part)
    if not rest.strip():
        return y + LH
    # rest of text in textbox starting after bold
    x1 = x0 + bw
    rc = pymupdf.Rect(x1, y, ML + TW, A4H - MB - 5)
    if rc.width > 10 and rc.height > FS:
        page.insert_textbox(rc, rest,
                            fontname=FONTR, fontsize=FS,
                            lineheight=1.5,
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # estimate total height: bold occupies first partial line, rest wraps
    # rough: (len(bold_part) + len(rest)) / CPL_INDENT lines
    total_chars = len(bold_part) + len(rest)
    n = max(1, round(total_chars / CPL_INDENT))
    return y + n * LH

def draw_bullet(page, text, y):
    BULL_X = ML + 14
    TEXT_X = ML + 42
    page.insert_text((BULL_X, y + FS), chr(0x2022), fontname=FONTR, fontsize=FS)
    rc = pymupdf.Rect(TEXT_X, y, ML + TW, A4H - MB - 5)
    if rc.height > FS:
        page.insert_textbox(rc, text,
                            fontname=FONTR, fontsize=FS,
                            lineheight=1.5,
                            align=pymupdf.TEXT_ALIGN_JUSTIFY)
    n = count_lines(text, CPL_BULLET)
    return y + n * LH

def gap(y, f=0.5):
    return y + LH * f

# ══════════════════════════════════════════════════════════════════════════════
doc = pymupdf.open()

def ensure_fonts(page):
    """Register Times New Roman on this page if not already done."""
    page.insert_font(fontname=FONTR, fontfile=FONTR_FILE)
    page.insert_font(fontname=FONTB, fontfile=FONTB_FILE)

def new_page():
    pg = doc.new_page(width=A4W, height=A4H)
    ensure_fonts(pg)
    return pg

# ── PAGE 1 ────────────────────────────────────────────────────────────────────
pg = new_page()
y = MT

y = draw_bold_para(pg, 'Цель работы: ',
    'создать сборочные чертежи в NanoCAD, соблюдая ГОСТ 2.109-73. '
    'Соблюсти все размеры, требования к оформлению сборочного чертежа, '
    'технические требования, требования к спецификации в соответствии '
    'с ГОСТ 2.108-68, а также допуски и элементы сварки.', y)
y = gap(y)

y = draw_bold(pg, 'Ход работы:', y)
y = gap(y)

y = draw_para(pg,
    'В ходе работы был создан сборочный чертёж в соответствии с требованиями ГОСТ, '
    'который содержит следующие элементы: изображение сборочной единицы, размеры, '
    'номера позиций, технические требования.', y)
y = gap(y)

y = draw_para(pg,
    'Все размеры, указанные в сборочном чертеже, разделены по следующим категориям '
    '(при необходимости): габаритные, установленные и присоединительные, '
    'эксплуатационные и монтажные.', y)
y = gap(y)

y = draw_para(pg,
    'Общие требования к сборочным чертежам, которые были учтены при выполнении задания:', y)

for b in [
    'все поверхности сопрягаемых деталей в месте соединения необходимо обозначить одной контурной линией;',
    'смежные детали в разрезах и сечениях обозначают штриховкой в различных направлениях;',
    'если число деталей больше двух — направление и частота штриховки меняется;',
    'сплошные детали в секущей плоскости вдоль оси или вдоль длинной стороны не штрихуются;',
    'собранные в сборочную единицу отдельные детали изображаются в рабочем положении;',
    'цельные, непустотелые детали изображаются в продольных разрезах незаштрихованными;',
    'для упрощения чтения сборочных чертежей на них допускается помещать изображение пограничных элементов и их размеры;',
    'линии невидимого контура применяют только для изображения простых элементов, '
    'когда выполнение разреза не упрощает чтение чертежа, а увеличивает его трудоёмкость;',
]:
    y = draw_bullet(pg, b, y)

# ── PAGE 2 ────────────────────────────────────────────────────────────────────
pg = new_page()
y = MT

for b in [
    'на сборочных чертежах перемещающиеся в работе части допускается изображать в крайнем '
    'или промежуточном положении с указанием соответствующего размера;',
    'клапанные устройства принято изображать закрытыми.',
]:
    y = draw_bullet(pg, b, y)
y = gap(y)

y = draw_para(pg,
    'Для изображений сборочных единиц существуют отдельные требования оформления, '
    'которые также были учтены при выполнении данной работы. К ним относятся:', y)

for b in [
    'количество изображений должно быть минимальным, но раскрывающим информацию '
    'о форме, расположении и характере соединения деталей;',
    'при разрезах все смежные детали необходимо заштриховать в противоположные стороны;',
    'на всех изображениях одна и та же деталь должна иметь одинаковую штриховку;',
    'на разрезах стандартные изделия не заштриховываются.',
]:
    y = draw_bullet(pg, b, y)
y = gap(y)

y = draw_para(pg,
    'К оформлению размеров на сборочных чертежах предъявляются следующие требования:', y)

for b in [
    'указываются габаритные размеры изделия, определяющие его внешние очертания;',
    'указываются установочные и присоединительные размеры, характеризующие установку '
    'изделия на месте его монтажа или присоединения к другому изделию;',
    'указываются другие необходимые и справочные размеры;',
    'все справочные размеры на чертеже отмечают знаком «*», а в технических требованиях '
    'выполняется надпись «*Размеры для справок».',
]:
    y = draw_bullet(pg, b, y)
y = gap(y)

y = draw_para(pg,
    'Помимо всего прочего, были учтены технические требования, включающие: '
    'подтверждение материала сертификатом при входном контроле, обеспечение '
    'идентификации материала на всех этапах технологического процесса, '
    'а также требования к сварным швам по ГОСТ 14771-76.', y)

# ── PAGE 3 ────────────────────────────────────────────────────────────────────
pg = new_page()
y = MT

y = draw_para(pg,
    'В ходе работы выполнены требования к спецификации, которые были освещены '
    'в презентации преподавателем (разделы, графы, позиционирование). '
    'В спецификацию входят разделы: документация, детали, стандартные изделия.', y)
y = gap(y)

y = draw_para(pg,
    'Также были учтены допуски и особенности сварки. '
    'Сварные швы выполнены по ГОСТ 14771-76 (сварка в защитных газах). '
    'Условные обозначения сварных швов проставлены на сборочных чертежах '
    'в соответствии с ГОСТ 2.312-72.', y)
y = gap(y)

y = draw_para(pg,
    'Таким образом, учитывая все особенности и нюансы работы, были выполнены '
    'сборочные чертежи трёх элементов (Балка 2А.012.001 СБ, '
    'Подставка 1 2А.012.002 СБ, Подставка 2 2А.012.003 СБ) '
    'и спецификации к ним. Результат работы представлен ниже.', y)
y = gap(y, 1.0)

y = draw_bold_para(pg, 'Вывод: ',
    'в ходе выполнения данной практической работы были созданы сборочные чертежи '
    'в NanoCAD с соблюдением ГОСТ 2.109-73. Были соблюдены все размеры, требования '
    'к оформлению сборочного чертежа, технические требования, требования к спецификации '
    'в соответствии с ГОСТ 2.108-68, а также допуски и элементы сварки.', y)

# ══════════════════════════════════════════════════════════════════════════════
# MERGE drawings + specs
# ══════════════════════════════════════════════════════════════════════════════

chert = pymupdf.open(os.path.join(BASE, 'L3', 'Практика 3.pdf'))
spec  = pymupdf.open(os.path.join(BASE, 'L3', 'Спец.pdf'))

for i in range(3):
    doc.insert_pdf(chert, from_page=i, to_page=i)
    doc.insert_pdf(spec,  from_page=i, to_page=i)

out = os.path.join(BASE, 'отчёт_пр3.pdf')
doc.save(out, garbage=4, deflate=True)
print(f'Saved: {out}')
print(f'Total pages: {doc.page_count}')
for i in range(doc.page_count):
    r = doc[i].rect
    orient = 'landscape' if r.width > r.height else 'portrait'
    print(f'  p{i+1}: {r.width:.0f}x{r.height:.0f} ({orient})')
