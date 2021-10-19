import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom
import datetime

from Class.Crud import ClassCrud
from Forms.Ciclo.ConsultaCiclo import Ui_ConsultaCiclo

import sqlite3


class ControllerAsistencias(object):
    def __init__(self, Dialog, QDialog):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_buscar_asistencia.textChanged.connect(
            lambda: self.search())
        self.Dialog.checkBox.stateChanged.connect(
            lambda: self.search())
        self.Dialog.tx_date.dateChanged.connect(
            lambda: self.search())

        self.Dialog.tx_buscar_asistencia.setFocus(True)
        self.Dialog.tx_date.setDate(datetime.datetime.now())

        self.Dialog.tableWidget.setColumnHidden(0, True)
        self.Dialog.tableWidget.setColumnHidden(15, True)

        header = self.Dialog.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(115)
        header.resizeSection(2, 150)
        header.resizeSection(3, 150)
        # header.resizeSection(7, 150)
        header.resizeSection(9, 180)
        header.resizeSection(10, 160)
        header.resizeSection(11, 115)
        header.resizeSection(12, 160)
        header.resizeSection(13, 160)
        header.resizeSection(14, 200)

        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        self.loadData()

    def loadData(self, _query="SELECT tb_asistencias.id_asistencia, tb_asistencias.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_asistencias.hora_entrada, tb_asistencias.hora_salida, tb_asistencias.tardanza, tb_asistencias.restante, tb_divisiones.division, tb_materias.materia, tb_asistencias.estado, tb_asistencias.fecha, tb_ciclos.ciclo, tb_sedes.sede,  tb_asistencias.observacion FROM tb_asistencias LEFT JOIN tb_profesores ON tb_asistencias.dni_profesor=tb_profesores.dni_profesor LEFT JOIN tb_sedes ON tb_asistencias.id_sede=tb_sedes.id_sede LEFT JOIN tb_ciclos ON tb_asistencias.id_ciclo=tb_ciclos.id_ciclo LEFT JOIN tb_clases ON tb_asistencias.id_clase = tb_clases.id_clase LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_materias ON tb_divisiones.id_materia = tb_materias.id_materia", filter = ""):
        if(filter != ""):
            _query += filter

        crud = ClassCrud()
        result = crud.Read(_query)

        self.Dialog.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Dialog.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Dialog.tableWidget.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def search(self):
        try:
            dateFilter =""
            dateObject = self.Dialog.tx_date.date().toPyDate()
            date = dateObject.strftime("%d-%m-%Y")

            if(self.Dialog.checkBox.isChecked() == True):
                dateFilter = " AND fecha = '" + date + "'"

            if str(self.Dialog.tx_buscar_asistencia.text()) == "":
                if(self.Dialog.checkBox.isChecked() == True):
                    self.loadData(filter=" Where fecha = '" + date + "'")
                else:
                    self.loadData()
            else:
                if (self.Dialog.radioButton_dni.isChecked() == True):
                    self.loadData(filter=" WHERE tb_asistencias.dni_profesor LIKE '" + str(self.Dialog.tx_buscar_asistencia.text() + "%'" + dateFilter))

                elif(self.Dialog.radioButton_apellido.isChecked() == True):
                    self.loadData(filter=" WHERE tb_profesores.apellido LIKE '" + str(self.Dialog.tx_buscar_asistencia.text() + "%'" + dateFilter))

                elif(self.Dialog.radioButton_nombre.isChecked() == True):
                    self.loadData(filter=" WHERE tb_profesores.nombre LIKE '" + str(self.Dialog.tx_buscar_asistencia.text() + "%'" + dateFilter))

                elif(self.Dialog.radioButton_entrada.isChecked() == True):
                    self.loadData(filter=" WHERE tb_asistencias.hora_entrada LIKE '" + str(self.Dialog.tx_buscar_asistencia.text() + "%'" + dateFilter))

                elif(self.Dialog.radioButton_salida.isChecked() == True):
                    self.loadData(filter=" WHERE tb_asistencias.hora_salida LIKE '" + str(self.Dialog.tx_buscar_asistencia.text() + "%'" + dateFilter))
        except Exception as e:
            print(e)
            return
