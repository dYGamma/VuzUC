import sys, os
import win32com.client

docx = os.path.abspath('Отчёт_Самарин_ГУАП_3510М.docx')
pdf = os.path.abspath('Отчёт_Самарин_ГУАП_3510М.pdf')

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    d = word.Documents.Open(docx)
    d.SaveAs(pdf, FileFormat=17)  # wdFormatPDF = 17
    d.Close(False)
    print('PDF saved:', pdf)
finally:
    word.Quit()
