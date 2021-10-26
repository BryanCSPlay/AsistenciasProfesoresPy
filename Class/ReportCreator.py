import os
# Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
                                Paragraph, Table, TableStyle)
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)

from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors

class ReportCreator(object):
    def __init__(self, data, title, nameFile, resumenList):
        self.data = data
        self.title = title
        self.nameFile = nameFile
        self.resumenList = resumenList

        # Title
        self.style = getSampleStyleSheet()
        self.styleTitle = ParagraphStyle('styleTitle',
                                   fontName="Helvetica-Bold",
                                   fontSize=16,
                                   parent=self.style['Heading2'],
                                   alignment=1,
                                   spaceAfter=14)

        self.createReport()

    def createReport(self):
        doc = SimpleDocTemplate(self.nameFile, pagesize=landscape(letter), rightMargin=10,
                                leftMargin=10, topMargin=10, bottomMargin=10)
        story = []

        print(self.data)
        print(type(self.data))
        tabla = Table(data=self.data,
                    style=[
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('BOX', (0, 0), (-1, -1), 2, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(red=(7.0/255),green=(70.0/255),blue=(124.0/255))),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white)
                    ]
                    )

        story.append(Paragraph(self.title, self.styleTitle))
        story.append(Spacer(0, 15))


        story.append(tabla)
        story.append(Spacer(0, 20))

        
        for i in self.resumenList:
            story.append(i)
            story.append(Spacer(0, 5))

        doc.build(story)

        os.system(self.nameFile)
