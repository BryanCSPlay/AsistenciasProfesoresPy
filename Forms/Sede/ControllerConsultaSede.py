import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Sede import ModelSede

import sqlite3

class ControllerConsultaSede(object):
    def __init__(self, Dialog, QDialog, modificar, id_sede):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.modificar = modificar
        self.id_sede = id_sede

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_sede)
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
        if (str(self.Dialog.tx_codigo.text()) != "" and str(self.Dialog.tx_sede.text()) != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_sedes WHERE id_sede ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_sede)
        self.Dialog.tx_sede.setText(str(result[1]))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oSede = ModelSede()
                if(self.modificar == False):
                    oSede.id_sede = int(self.Dialog.tx_codigo.text())
                    oSede.sede = str(self.Dialog.tx_sede.text())

                    query = 'INSERT OR REPLACE INTO tb_sedes (id_sede, sede) VALUES (?,?)'
                    crud = ClassCrud().Add(oSede.SedeToList(), query)

                    self.closeForm()
                else:
                    oSede.id_sede = int(self.Dialog.tx_codigo.text())
                    oSede.sede = str(self.Dialog.tx_sede.text())

                    row = (oSede.sede, oSede.id_sede)
                    query = 'UPDATE tb_sedes SET sede = ? WHERE id_sede = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Sedes")
        except Exception as e:
            print(e)
        '''except:
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Sedes")'''

    def closeForm(self):
        self.QDialog.close()