"""
Генерация отчёт_пр4.docx
Текст (А4 портрет) → чертежи и ведомости (разные форматы секций)
"""
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION_START
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import pymupdf, os

BASE    = r'C:\VuzUC\MAGA\Nstya_SECOND'
L4      = os.path.join(BASE, 'L4')
IMG_DIR = os.path.join(BASE, 'L4_pages_hq')
os.makedirs(IMG_DIR, exist_ok=True)

# ── Рендеринг страниц из PDF в PNG ────────────────────────────────────────────

def render_pdf(path, prefix, scale=2.0):
    """Рендерит все страницы PDF в PNG, возвращает список путей."""
    doc = pymupdf.open(path)
    paths = []
    for i in range(doc.page_count):
        pg   = doc[i]
        pix  = pg.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
        out  = os.path.join(IMG_DIR, f'{prefix}_p{i+1}.png')
        pix.save(out)
        paths.append(out)
        print(f'  Rendered: {out}')
    return paths

print('Rendering PDFs...')
chert_sb  = render_pdf(os.path.join(L4, 'Практика 4.pdf'), 'sb',  scale=2.0)   # A1 land
chert_gh  = render_pdf(os.path.join(L4, 'Практика.pdf'),   'gh',  scale=2.0)   # A2 land
spec_pages = render_pdf(os.path.join(L4, '333.pdf'),        'spec', scale=2.0)  # A4 port ×2
ved_pages  = render_pdf(os.path.join(L4, '444.pdf'),        'ved',  scale=2.0)  # A3 land ×3

# ── Вспомогательные функции ───────────────────────────────────────────────────

doc = Document()

sec0 = doc.sections[0]
sec0.left_margin   = Cm(3)
sec0.right_margin  = Cm(1.5)
sec0.top_margin    = Cm(2)
sec0.bottom_margin = Cm(2)


def set_spacing(p, line=1.5, sb=0, sa=0):
    pPr = p._p.get_or_add_pPr()
    spc = OxmlElement('w:spacing')
    spc.set(qn('w:line'),     str(int(line * 240)))
    spc.set(qn('w:lineRule'), 'auto')
    spc.set(qn('w:before'),   str(int(sb * 20)))
    spc.set(qn('w:after'),    str(int(sa * 20)))
    pPr.append(spc)


def add_run(p, text, bold=False):
    run = p.add_run(text)
    run.bold = bold
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rFonts.set(qn('w:cs'),    'Times New Roman')
    ex = rPr.find(qn('w:rFonts'))
    if ex is not None:
        rPr.remove(ex)
    rPr.insert(0, rFonts)
    return run


def new_para(indent=True, center=False):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center' if center else 'both')
    pPr.append(jc)
    ind = OxmlElement('w:ind')
    if indent:
        ind.set(qn('w:firstLine'), '709')
    pPr.append(ind)
    set_spacing(p)
    return p


def numbered_item(n, text):
    p = new_para(indent=False)
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:left'),    '709')
    ind.set(qn('w:hanging'), '709')
    add_run(p, f'{n}.\t{text}')
    return p


def add_image_section(img_path, pw_cm, ph_cm, img_w_cm,
                      lm=1.0, rm=1.0, tm=1.0, bm=1.0,
                      orient=WD_ORIENT.LANDSCAPE):
    """Добавляет новую секцию с изображением."""
    sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec.orientation  = orient
    sec.page_width   = Cm(pw_cm)
    sec.page_height  = Cm(ph_cm)
    sec.left_margin  = Cm(lm)
    sec.right_margin = Cm(rm)
    sec.top_margin   = Cm(tm)
    sec.bottom_margin= Cm(bm)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, sb=0, sa=0)
    p.add_run().add_picture(img_path, width=Cm(img_w_cm))


# ── ТЕКСТ ─────────────────────────────────────────────────────────────────────

p = new_para()
add_run(p, 'Цель работы: ', bold=True)
add_run(p, 'изучение оформления общего сборочного и габаритного чертежей в ПО NanoCAD, '
           'а также построения болтовых соединений и подготовки выходной документации.')

p = new_para()
add_run(p, 'Ход работы:', bold=True)

p = new_para()
add_run(p, 'План работы:', bold=True)

steps = [
    'Перенести чертёж общей сборки из SolidWorks в NanoCAD.',
    'Настроить необходимые проекции, разрезы и местные виды.',
    'Выбрать масштаб по ГОСТ.',
    'Выполнить болтовые соединения (болты, гайки, шайбы).',
    'Нанести размеры и позиции деталей для спецификации.',
    'Создать габаритный чертёж.',
    'Заполнить спецификацию, ведомость спецификаций и ведомость покупных изделий.',
    'Заполнить рамку чертежей и ведомостей.',
    'Оформить отчёт по ГОСТ.',
]
for i, s in enumerate(steps, 1):
    numbered_item(i, s)

p = new_para()
add_run(p, 'Описание работы:', bold=True)

p = new_para()
add_run(p, 'В SolidWorks для общей сборки был создан чертёж с необходимыми видами '
           'и разрезами в масштабе 1:1, после чего файл сохранён в формате «.dwg».')

p = new_para()
add_run(p, 'В NanoCAD были загружены чертежи деталей и подборов, затем перенесены '
           'проекции общей сборки во вкладку «модель».')

p = new_para()
add_run(p, 'В области листа выбран формат A2 и созданы видовые экраны с масштабами '
           'по ГОСТ для размещения чертежа общей сборки с выбранным масштабом.')

p = new_para()
add_run(p, 'После этого выполнено построение крепежных элементов: болтов, гаек и шайб.')

p = new_para()
add_run(p, 'Затем нанесены позиции деталей и сборочных единиц, размеры и отклонения. '
           'После этого выполнено выравнивание чертежа и заполнение основной надписи '
           'и технических требований.')

p = new_para()
add_run(p, 'Также создан габаритный чертёж, отражающий основные размеры изделия '
           'без позиционирования и местных видов.')

p = new_para()
add_run(p, 'Составлена спецификация, включающая сборочные единицы и стандартные '
           'крепежные изделия с их количеством. Далее оформлены ведомость спецификаций '
           'и ведомость покупных изделий, содержащая перечень используемого крепежа.')

p = new_para()
add_run(p, 'Вывод: ', bold=True)
add_run(p, 'в ходе работы был выполнен общий сборочный и габаритный чертежи. '
           'Выполнен перенос сборки из SolidWorks, оформлены чертежи в соответствии '
           'с ГОСТ, настроены масштабы, линии и шрифты, нанесены размеры и позиции деталей. '
           'Также были построены болтовые соединения, составлены спецификация, '
           'ведомость спецификаций и ведомость покупных изделий, а основная надпись '
           'заполнена необходимыми данными.')

# ── ЧЕРТЕЖИ И ВЕДОМОСТИ ───────────────────────────────────────────────────────

# Сборочный чертёж — А1 ландшафт (84.1 × 59.4 см)
add_image_section(chert_sb[0],
                  pw_cm=84.1, ph_cm=59.4, img_w_cm=82.1,
                  lm=1.0, rm=1.0, tm=1.0, bm=1.0,
                  orient=WD_ORIENT.LANDSCAPE)

# Габаритный чертёж — А2 ландшафт (59.4 × 42.0 см)
add_image_section(chert_gh[0],
                  pw_cm=59.4, ph_cm=42.0, img_w_cm=57.4,
                  lm=1.0, rm=1.0, tm=1.0, bm=1.0,
                  orient=WD_ORIENT.LANDSCAPE)

# Спецификация — А4 портрет (21 × 29.7 см) × 2 листа
for img in spec_pages:
    add_image_section(img,
                      pw_cm=21.0, ph_cm=29.7, img_w_cm=17.0,
                      lm=3.0, rm=1.5, tm=2.0, bm=2.0,
                      orient=WD_ORIENT.PORTRAIT)

# Ведомости — А3 ландшафт (42 × 29.7 см) × 3 листа
for img in ved_pages:
    add_image_section(img,
                      pw_cm=42.0, ph_cm=29.7, img_w_cm=40.0,
                      lm=1.0, rm=1.0, tm=1.0, bm=1.0,
                      orient=WD_ORIENT.LANDSCAPE)

# ── СОХРАНЕНИЕ ────────────────────────────────────────────────────────────────

out = os.path.join(BASE, 'отчёт_пр4.docx')
doc.save(out)
print(f'\nSaved: {out}')
print(f'Total sections: {len(doc.sections)}')
