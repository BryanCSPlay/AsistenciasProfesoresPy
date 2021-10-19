import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Materia import ModelMateria

import sqlite3


class ControllerConsultaMateria(object):
    def __init__(self, Dialog, QDialog, modificar, id_materia):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.modificar = modificar
        self.id_materia = id_materia

        self.load()


    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_materia)
        self.Dialog.Bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.Bt_cancelar.clicked.connect(lambda: self.closeForm())
        self.Dialog.tx_codigo.setEnabled(False)
        self.Dialog.tx_materia.setFocus(True)

        if self.modificar == True:
            self.getData()

    #########################################################################################

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_codigo.setValidator(self.onlyInt)

    def validationData(self):
        if (self.Dialog.tx_codigo.text() != "" and self.Dialog.tx_materia.text() != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_materias WHERE id_materia ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_materia)
        self.Dialog.tx_materia.setText(str(result[1]))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oMateria = ModelMateria()
                if(self.modificar == False):
                    oMateria.id_materia = int(self.Dialog.tx_codigo.text())
                    oMateria.materia = str(self.Dialog.tx_materia.text())

                    query = 'INSERT OR REPLACE INTO tb_materias (id_materia, materia) VALUES (?,?)'
                    crud = ClassCrud().Add(oMateria.MateriaToList(), query)

                    self.closeForm()
                else:
                    oMateria.id_materia = int(self.Dialog.tx_codigo.text())
                    oMateria.materia = str(self.Dialog.tx_materia.text())

                    row = (oMateria.materia,
                           oMateria.id_materia)
                    query = 'UPDATE tb_materias SET materia = ? WHERE id_materia = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Materia")
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Materia")

    def closeForm(self):
        self.QDialog.close()