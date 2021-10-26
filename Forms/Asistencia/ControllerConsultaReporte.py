import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom
import datetime

import os
# Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
                                Paragraph, Table, TableStyle)
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)

from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors


from Class.ReportCreator import ReportCreator
from Class.Crud import ClassCrud
from Forms.Division.Division import Ui_Divisiones
from Forms.Profesor.Profesores import Ui_Profesores

import threading


class ControllerConsultaReporte(object):
    def __init__(self, Dialog, QDialog):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.load()

        # threading.Thread(target=self.createReport).start()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.bt_guardar.clicked.connect(self.calculateReport)
        self.Dialog.bt_cancelar.clicked.connect(self.closeForm)

        self.Dialog.tx_codigo_division.textChanged.connect(
            lambda: self.searchDivisionWithId())
        self.Dialog.tx_dni_profesor.textChanged.connect(
            lambda: self.searchProfesorWithId())

        self.Dialog.bt_division.clicked.connect(
            lambda: self.openFormSearchIdDivision())
        self.Dialog.bt_profesor.clicked.connect(
            lambda: self.openFormSearchDniProfesor())
        self.Dialog.tx_codigo_division.setFocus(True)

    def calculateReport(self):
        query = "SELECT tb_asistencias.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_asistencias.hora_entrada, tb_asistencias.hora_salida, tb_asistencias.tardanza, tb_asistencias.restante, tb_divisiones.division, tb_materias.materia, tb_asistencias.estado, tb_asistencias.fecha FROM tb_asistencias LEFT JOIN tb_profesores ON tb_asistencias.dni_profesor=tb_profesores.dni_profesor LEFT JOIN tb_sedes ON tb_asistencias.id_sede=tb_sedes.id_sede LEFT JOIN tb_ciclos ON tb_asistencias.id_ciclo=tb_ciclos.id_ciclo LEFT JOIN tb_clases ON tb_asistencias.id_clase = tb_clases.id_clase LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_materias ON tb_divisiones.id_materia = tb_materias.id_materia WHERE "
        if(str(self.Dialog.tx_codigo_division.text()) != "" and str(self.Dialog.lb_division.text()) != ""):
            query += str("tb_divisiones.id_division == " + "'" +
                         str(self.Dialog.tx_codigo_division.text()) + "'")
        else:
            query += str(" tb_divisiones.id_division == " + "'" + str(self.Dialog.tx_codigo_division.text()) +
                         "' OR tb_divisiones.id_division != " + "'" + str(self.Dialog.tx_codigo_division.text()) + "'")

        if(str(self.Dialog.tx_dni_profesor.text()) != "" and str(self.Dialog.lb_profesor.text()) != ""):
            query += str(" AND tb_asistencias.dni_profesor == " +
                         "'" + str(self.Dialog.tx_dni_profesor.text()) + "'")

        if(self.Dialog.comboBox_mes.currentIndex() != 0):
            now = datetime.datetime.now()
            queryDate = " AND strftime('%m', (substr(tb_asistencias.fecha, 7, 4) || '-' || substr(tb_asistencias.fecha, 4, 2) || '-' || substr(tb_asistencias.fecha, 1, 2))) = '" + str(self.Dialog.comboBox_mes.currentIndex(
            )) + "' and strftime('%Y', (substr(tb_asistencias.fecha, 7, 4) || '-' || substr(tb_asistencias.fecha, 4, 2) || '-' || substr(tb_asistencias.fecha, 1, 2))) = '" + str(now.year) + "'"
            query += queryDate

        if(self.Dialog.bt_lunes.isChecked() == True):
            query += " AND tb_clases.dia == 'Lunes'"
        elif(self.Dialog.bt_martes.isChecked() == True):
            query += " AND tb_clases.dia == 'Martes'"
        elif(self.Dialog.bt_miercoles.isChecked() == True):
            query += " AND tb_clases.dia == 'Miércoles'"
        elif(self.Dialog.bt_jueves.isChecked() == True):
            query += " AND tb_clases.dia == 'Jueves'"
        elif(self.Dialog.bt_viernes.isChecked() == True):
            query += " AND tb_clases.dia == 'Viernes'"
        elif(self.Dialog.bt_sabado.isChecked() == True):
            query += " AND tb_clases.dia == 'Sábado'"

        if(self.Dialog.bt_dentro.isChecked() == True):
            query += " AND tb_asistencias.estado == 'Dentro del instituto'"
        elif(self.Dialog.bt_fuera.isChecked() == True):
            query += " AND tb_asistencias.estado == 'Fuera del instituto'"
        elif(self.Dialog.bt_ausencia.isChecked() == True):
            query += " AND tb_asistencias.estado == 'Ausencia'"
        elif(self.Dialog.bt_recuperacion.isChecked() == True):
            query += " AND tb_asistencias.estado == 'Recuperación'"

        self.createReport(str(query))

    def createReport(self, query):
        crud = ClassCrud()
        #print(str(query))
        #queryReportAllAssintance = "SELECT tb_asistencias.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_asistencias.hora_entrada, tb_asistencias.hora_salida, tb_asistencias.tardanza, tb_asistencias.restante, tb_divisiones.division, tb_materias.materia, tb_asistencias.estado, tb_asistencias.fecha FROM tb_asistencias LEFT JOIN tb_profesores ON tb_asistencias.dni_profesor=tb_profesores.dni_profesor LEFT JOIN tb_sedes ON tb_asistencias.id_sede=tb_sedes.id_sede LEFT JOIN tb_ciclos ON tb_asistencias.id_ciclo=tb_ciclos.id_ciclo LEFT JOIN tb_clases ON tb_asistencias.id_clase = tb_clases.id_clase LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_materias ON tb_divisiones.id_materia = tb_materias.id_materia"
        resultList = crud.Read(query).fetchall()
        reporHeaderData = ('DNI', 'Apellido', 'Nombre', 'Entrada', 'Salida',
                           'Tardanza', 'Restante', 'División', 'Materia', 'Estado', 'Fecha')
        resultList.insert(0, reporHeaderData)

        # print(resultList)

        resumenList = self.generateListResumen(resultList)

        report = ReportCreator(resultList, "Asistencias",
                               "Asistencias.pdf", resumenList)

    def generateListResumen(self, resultList):
        style = getSampleStyleSheet()
        styleResumen = ParagraphStyle('styleTitle',
                                      fontName="Helvetica",
                                      fontSize=10,
                                      parent=style['Heading6'],
                                      alignment=0,
                                      spaceAfter=0)

        styleResumenEnd = ParagraphStyle('styleTitle',
                                         fontName="Helvetica",
                                         fontSize=10,
                                         parent=style['Heading6'],
                                         alignment=0,
                                         spaceAfter=14)

        countAsistencia = 0
        countAusencia = 0
        countRecuperacion = 0
        sumTardanza = datetime.timedelta(hours=0, minutes=0, seconds=0)
        sumRestante = datetime.timedelta(hours=0, minutes=0, seconds=0)

        for i in resultList:
            if(i[9] == "Dentro del instituto"):
                countAsistencia = countAsistencia + 1
            elif(i[9] == "Fuera del instituto"):
                countAsistencia = countAsistencia + 1
            elif(i[9] == "Recuperación"):
                countRecuperacion = countRecuperacion + 1
            elif(i[9] == "Ausencia"):
                countAusencia = countAusencia + 1

            tardanza = i[5].split(":")
            restante = i[6].split(":")

            if(str(i[5]) != "" and str(i[5]) != "Tardanza" and str(i[5]) != "No aplica"):
                sumTardanza = sumTardanza + datetime.timedelta(hours=float(tardanza[0]), minutes=float(tardanza[1]), seconds=float(tardanza[2]))
            if(str(i[6]) != "" and str(i[6]) != "Restante" and str(i[5]) != "No aplica"):
                sumRestante = sumRestante + datetime.timedelta(hours=float(restante[0]), minutes=float(restante[1]), seconds=float(restante[2]))

        resumenList = []
        sumTardanzaSplit = str(sumTardanza).split(":")
        sumRestanteSplit = str(sumRestante).split(":")

        if(self.Dialog.checkBox_ausencias.isChecked() == True):
            resumenList.append(Paragraph("-  Hay una cantidad de <b>"+ str(countAusencia) +"</b> clases en la que se marcó ausencia.", styleResumen))
        if(self.Dialog.checkBox_asistencias.isChecked() == True):
            resumenList.append(Paragraph("-  Hay una cantidad de <b>"+ str(countAsistencia) +"</b> estados de asistencia (Dentro-Fuera del instituto)", styleResumen))
        if(self.Dialog.checkBox_recuperaciones.isChecked() == True):
            resumenList.append(Paragraph("-  Hay una cantidad de <b>"+ str(countRecuperacion) +"</b> clases de tipo recuperación en total.", styleResumen))
        if(self.Dialog.checkBox_tardanzas.isChecked() == True):
            resumenList.append(Paragraph("-  Hay una cantidad de <b>"+ str(sumTardanzaSplit[0])+ " horas "+ str(sumTardanzaSplit[1]) +" minutos y "+ str(sumTardanzaSplit[2]) +" segundos" +"</b>  de tiempo en tardanza.", styleResumen))
        if(self.Dialog.checkBox_restantes.isChecked() == True):
            resumenList.append(Paragraph("-  Hay una cantidad de <b>"+ str(sumRestanteSplit[0])+  " horas "+ str(sumRestanteSplit[1]) +" minutos y "+ str(sumRestanteSplit[2]) +" segundos" +"</b>  de tiempo restante.", styleResumenEnd))

        return resumenList

    def searchDivisionWithId(self):
        try:
            if str(self.Dialog.tx_codigo_division.text()) == "":
                self.Dialog.lb_division.setText("")
            else:
                id = self.Dialog.tx_codigo_division.text()
                query = "SELECT division FROM tb_divisiones WHERE id_division = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_division.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_division.text() == " None"):
                    self.Dialog.lb_division.setText("")
        except Exception as e:
            print(e)

    def searchProfesorWithId(self):
        try:
            if str(self.Dialog.tx_dni_profesor.text()) == "":
                self.Dialog.lb_profesor.setText("")
            else:
                id = self.Dialog.tx_dni_profesor.text()
                query = "SELECT apellido, nombre FROM tb_profesores WHERE dni_profesor = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_profesor.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_profesor.text() == " None"):
                    self.Dialog.lb_profesor.setText("")
        except Exception as e:
            print(e)

    def openFormSearchIdDivision(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Divisiones()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_codigo_division)
        ventana.exec_()

    def openFormSearchDniProfesor(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Profesores()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_dni_profesor)
        ventana.exec_()

    def closeForm(self):
        self.QDialog.close()
