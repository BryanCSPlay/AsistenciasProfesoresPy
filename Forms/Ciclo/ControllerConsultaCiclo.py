import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Ciclo import ModelCiclo

import sqlite3

class ControllerConsultaCiclo(object):
    def __init__(self, Dialog, QDialog, modificar, id_ciclo):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.modificar = modificar
        self.id_ciclo = id_ciclo

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_ciclo)
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
        if (str(self.Dialog.tx_codigo.text()) != "" and str(self.Dialog.tx_ciclo.text()) != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_ciclos WHERE id_ciclo ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_ciclo)
        self.Dialog.tx_ciclo.setText(str(result[1]))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oCiclo = ModelCiclo()
                if(self.modificar == False):
                    oCiclo.id_ciclo = int(self.Dialog.tx_codigo.text())
                    oCiclo.ciclo = str(self.Dialog.tx_ciclo.text())

                    query = 'INSERT OR REPLACE INTO tb_ciclos (id_ciclo, ciclo) VALUES (?,?)'
                    crud = ClassCrud().Add(oCiclo.CicloToList(), query)

                    self.closeForm()
                else:
                    oCiclo.id_ciclo = int(self.Dialog.tx_codigo.text())
                    oCiclo.ciclo = str(self.Dialog.tx_ciclo.text())

                    row = (oCiclo.ciclo, oCiclo.id_ciclo)
                    query = 'UPDATE tb_ciclos SET ciclo = ? WHERE id_ciclo = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Ciclo")
        except Exception as e:
            print(e)
        '''except:
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Ciclo")'''

    def closeForm(self):
        self.QDialog.close()