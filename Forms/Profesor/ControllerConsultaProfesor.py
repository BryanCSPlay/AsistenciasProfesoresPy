from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom
import qrcode
import os
from PIL import Image

from Class.Crud import ClassCrud
from Models.Profesor import ModelProfesor

import sqlite3

class ControllerConsultaProfesor(object):
    def __init__(self, Dialog, QDialog, modificar, id_profesor):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.modificar = modificar
        self.id_profesor = id_profesor
        self.tx_codigo_anterior = self.id_profesor

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_profesor)
        self.Dialog.tx_codigo.textChanged.connect(lambda: self.generatorQr())
        self.Dialog.bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.bt_cancelar.clicked.connect(lambda: self.closeForm())
        self.Dialog.tx_codigo.setEnabled(True)
        self.Dialog.tx_codigo.setFocus(True)
        self.Dialog.tx_fn.setDate(QtCore.QDate.currentDate())
        self.generatorQr()

        if self.modificar == True:
            self.Dialog.tx_codigo.setEnabled(False)
            self.getData()

    #########################################################################################
    def generatorQr(self):
        try:
            os.remove(self.tx_codigo_anterior)
        except Exception as e:
            print(e)

        cadena = self.encryptQr(self.Dialog.tx_codigo.text())

        imagen = qrcode.make(cadena)

        nombre_imagen = self.Dialog.tx_codigo.text() + ".PNG"
        archivo_imagen = open("qr/" + nombre_imagen, "wb")
        imagen.save("qr/" + nombre_imagen)

        archivo_imagen.close()

        pixmap = QtGui.QPixmap("qr/" + self.Dialog.tx_codigo.text() + ".PNG")
        self.tx_codigo_anterior = "qr/" + self.Dialog.tx_codigo.text() + ".PNG"

        w = self.Dialog.tx_qr.width()
        h = self.Dialog.tx_qr.height()

        # set a scaled pixmap to a w x h window keeping its aspect ratio
        self.Dialog.tx_qr.setPixmap(pixmap.scaled(w, h,  QtCore.Qt.KeepAspectRatio))

    def encryptQr(self, num):
        x1 = num.replace("1", "ACE")
        x2 = x1.replace("2", "GIK")
        x3 = x2.replace("3", "MÑP")
        x4 = x3.replace("4", "RTV")
        x5 = x4.replace("5", "XZB")
        x6 = x5.replace("6", "DFH")
        x7 = x6.replace("7", "JLN")
        x8 = x7.replace("8", "OQS")
        x9 = x8.replace("9", "UWX")
        x0 = x9.replace("0", "YÑX")

        return x0

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_codigo.setValidator(self.onlyInt)

    def validationData(self):
        if (self.Dialog.tx_codigo.text() != "" and self.Dialog.tx_apellido.text() != "" and self.Dialog.tx_nombre.text() != "" and self.Dialog.tx_fn.text != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_profesores WHERE dni_profesor ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_profesor)
        self.Dialog.tx_apellido.setText(str(result[1]))
        self.Dialog.tx_nombre.setText(str(result[2]))
        self.Dialog.tx_fn.setDate(datetime.strptime(result[3], '%d/%m/%Y'))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oProfesor = ModelProfesor()
                if(self.modificar == False):
                    oProfesor.dni_profesor = int(self.Dialog.tx_codigo.text())
                    oProfesor.apellido = str(self.Dialog.tx_apellido.text())
                    oProfesor.nombre = str(self.Dialog.tx_nombre.text())
                    oProfesor.fn = str(self.Dialog.tx_fn.text())
                    oProfesor.qr = self.encryptQr(self.Dialog.tx_codigo.text())

                    query = 'INSERT INTO tb_profesores (dni_profesor, apellido, nombre, fn, qr) VALUES (?,?,?,?,?)'
                    crud = ClassCrud().Add(oProfesor.ProfesorToList(), query)

                    self.QDialog.close()
                else:
                    oProfesor.dni_profesor = int(self.Dialog.tx_codigo.text())
                    oProfesor.apellido = str(self.Dialog.tx_apellido.text())
                    oProfesor.nombre = str(self.Dialog.tx_nombre.text())
                    oProfesor.fn = str(self.Dialog.tx_fn.text())
                    oProfesor.qr = self.encryptQr(self.Dialog.tx_codigo.text())

                    row = (oProfesor.apellido, oProfesor.nombre,
                           oProfesor.fn, oProfesor.qr, oProfesor.dni_profesor)
                    query = 'UPDATE tb_profesores SET apellido = ?, nombre = ?, fn = ?, qr = ? WHERE dni_profesor = ?'
                    crud = ClassCrud().Update(row, query)

                    self.QDialog.close()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Profesor")
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro, verifique que el dni no pertenezca a otra registro", "Profesor")

    def closeForm(self):
        try:
            os.remove(self.tx_codigo_anterior)
        except Exception as e:
            print(e)
        self.QDialog.close()
