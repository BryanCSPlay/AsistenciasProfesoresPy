import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Clase import ModelClase

from Forms.Division.Division import Ui_Divisiones
from Forms.Profesor.Profesores import Ui_Profesores

import sqlite3

class ControllerConsultaClase(object):
    def __init__(self, Dialog, QDialog, modificar, id_clase):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.modificar = modificar
        self.id_clase = id_clase

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo_division.textChanged.connect(
            lambda: self.searchDivisionWithId())
        self.Dialog.tx_dni_profesor.textChanged.connect(
            lambda: self.searchProfesorWithId())

        self.Dialog.bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.bt_cancelar.clicked.connect(lambda: self.closeForm())
        self.Dialog.bt_division.clicked.connect(
            lambda: self.openFormSearchIdDivision())
        self.Dialog.bt_profesor.clicked.connect(
            lambda: self.openFormSearchDniProfesor())
        self.Dialog.tx_codigo_division.setFocus(True)

        if self.modificar == True:
            self.getData()

    #########################################################################################

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_dni_profesor.setValidator(self.onlyInt)
        self.Dialog.tx_codigo_division.setValidator(self.onlyInt)

    def validationData(self):
        if (self.Dialog.lb_division.text() != "" and self.Dialog.lb_profesor.text() != ""
                and self.Dialog.tx_entrada.text() != "" and self.Dialog.tx_salida.text() != ""):

            if(self.Dialog.bt_lunes.isChecked() == False and self.Dialog.bt_martes.isChecked() == False and
                self.Dialog.bt_miercoles.isChecked() == False and self.Dialog.bt_jueves.isChecked() == False and
                self.Dialog.bt_viernes.isChecked() == False and self.Dialog.bt_sabado.isChecked() == False):
                return False
            else:
                return True
        else:
            return False

    def getData(self):
        query = "select * from tb_clases WHERE id_clase ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_clase)
        self.Dialog.tx_codigo_division.setText(str(result[1]))
        self.Dialog.tx_dni_profesor.setText(str(result[2]))

        timeEntrada = QtCore.QTime(
            int((result[3])[0:2]), int((result[3])[3:5]))
        timeSalida = QtCore.QTime(int((result[4])[0:2]), int((result[4])[3:5]))

        self.Dialog.tx_entrada.setTime(timeEntrada)
        self.Dialog.tx_salida.setTime(timeSalida)

        if(result[5] == "Lunes"):
            self.Dialog.bt_lunes.setChecked(True)
        elif(result[5] == "Martes"):
            self.Dialog.bt_martes.setChecked(True)
        elif(result[5] == "Miercoles"):
            self.Dialog.bt_miercoles.setChecked(True)
        elif(result[5] == "Jueves"):
            self.Dialog.bt_jueves.setChecked(True)
        elif(result[5] == "Viernes"):
            self.Dialog.bt_viernes.setChecked(True)
        elif(result[5] == "Sábado"):
            self.Dialog.bt_sabado.setChecked(True)

        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oClase = ModelClase()
                if(self.modificar == False):
                    oClase.id_division = int(self.Dialog.tx_codigo_division.text())
                    oClase.dni_profesor = str(self.Dialog.tx_dni_profesor.text())
                    oClase.hora_entrada = str(self.Dialog.tx_entrada.text())
                    oClase.hora_salida = str(self.Dialog.tx_salida.text())

                    if(self.Dialog.bt_lunes.isChecked()):
                        oClase.dia = "Lunes"
                    elif(self.Dialog.bt_martes.isChecked()):
                        oClase.dia = "Martes"
                    elif(self.Dialog.bt_miercoles.isChecked()):
                        oClase.dia = "Miércoles"
                    elif(self.Dialog.bt_jueves.isChecked()):
                        oClase.dia = "Jueves"
                    elif(self.Dialog.bt_viernes.isChecked()):
                        oClase.dia = "Viernes"
                    elif(self.Dialog.bt_sabado.isChecked()):
                        oClase.dia = "Sábado"

                    query = 'INSERT OR REPLACE INTO tb_clases (id_division, dni_profesor, entrada, salida, dia) VALUES (?,?,?,?,?)'
                    crud = ClassCrud().Add(oClase.ClaseToList(), query)

                    self.closeForm()
                else:
                    oClase.id_division = int(self.Dialog.tx_codigo_division.text())
                    oClase.dni_profesor = str(self.Dialog.tx_dni_profesor.text())
                    oClase.hora_entrada = str(self.Dialog.tx_entrada.text())
                    oClase.hora_salida = str(self.Dialog.tx_salida.text())

                    if(self.Dialog.bt_lunes.isChecked()):
                        oClase.dia = "Lunes"
                    elif(self.Dialog.bt_martes.isChecked()):
                        oClase.dia = "Martes"
                    elif(self.Dialog.bt_miercoles.isChecked()):
                        oClase.dia = "Miércoles"
                    elif(self.Dialog.bt_jueves.isChecked()):
                        oClase.dia = "Jueves"
                    elif(self.Dialog.bt_viernes.isChecked()):
                        oClase.dia = "Viernes"
                    elif(self.Dialog.bt_sabado.isChecked()):
                        oClase.dia = "Sábado"

                    row = (oClase.id_division, oClase.dni_profesor,
                           oClase.hora_entrada, oClase.hora_salida,
                           oClase.dia, self.id_clase)
                    query = 'UPDATE tb_clases SET id_division = ?, dni_profesor = ?, entrada = ?, salida = ? , dia = ? WHERE id_clase = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Clase")
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Clase")

    def closeForm(self):
        self.QDialog.close()

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
