import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Carrera import ModelCarrera

import sqlite3

class ControllerConsultaCarrera(object):
    def __init__(self, Dialog, QDialog, modificar, id_carrera):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.modificar = modificar
        self.id_carrera = id_carrera

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_carrera)
        self.Dialog.Bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.Bt_cancelar.clicked.connect(lambda: self.closeForm())

        if self.modificar == True:
            self.getData()

    #########################################################################################

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_codigo.setValidator(self.onlyInt)
        self.Dialog.tx_codigo.setEnabled(False)

    def validationData(self):
        if (str(self.Dialog.tx_codigo.text()) != "" and str(self.Dialog.tx_nombre.text()) != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_carreras WHERE id_carrera ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_carrera)
        self.Dialog.tx_nombre.setText(str(result[1]))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oCarrera = ModelCarrera()
                if(self.modificar == False):
                    oCarrera.id_carrera = int(self.Dialog.tx_codigo.text())
                    oCarrera.carrera = str(self.Dialog.tx_nombre.text())

                    query = 'INSERT OR REPLACE INTO tb_carreras (id_carrera, carrera) VALUES (?,?)'
                    crud = ClassCrud().Add(oCarrera.CarreraToList(), query)

                    self.closeForm()
                else:
                    oCarrera.id_carrera = int(self.Dialog.tx_codigo.text())
                    oCarrera.carrera = str(self.Dialog.tx_nombre.text())

                    row = (oCarrera.carrera, oCarrera.id_carrera)
                    query = 'UPDATE tb_carreras SET carrera = ? WHERE id_carrera = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Carrera")
        except Exception as e:
            print(e)
        '''except:
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Carrera")'''

    def closeForm(self):
        self.QDialog.close()