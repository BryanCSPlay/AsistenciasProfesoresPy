import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Models.Division import ModelDivision
from Forms.Materia.Materias import Ui_Materias

import sqlite3

class ControllerConsultaDivision(object):
    def __init__(self, Dialog, QDialog, modificar, id_division):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.modificar = modificar
        self.id_division = id_division

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo.setText(self.id_division)
        self.Dialog.tx_id_materia.textChanged.connect(
            lambda: self.searchMateriaWithId())
        self.Dialog.bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.bt_cancelar.clicked.connect(lambda: self.closeForm())
        self.Dialog.bt_id_materia.clicked.connect(lambda: self.openFormSearchId())
        self.Dialog.tx_codigo.setEnabled(False)
        self.Dialog.tx_nombre.setFocus(True)

        if self.modificar == True:
            self.getData()

    #########################################################################################

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_codigo.setValidator(self.onlyInt)
        self.Dialog.tx_id_materia.setValidator(self.onlyInt)

    def validationData(self):
        if (self.Dialog.tx_codigo.text() != "" and self.Dialog.tx_nombre.text() != "" and self.Dialog.tx_id_materia.text() != ""):
            return True
        else:
            return False

    def getData(self):
        query = "select * from tb_divisiones WHERE id_division ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_division)
        self.Dialog.tx_nombre.setText(str(result[1]))
        self.Dialog.tx_id_materia.setText(str(result[2]))
        crud.connection.close()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                oDivision = ModelDivision()
                if(self.modificar == False):
                    oDivision.id_division = int(self.Dialog.tx_codigo.text())
                    oDivision.division = str(self.Dialog.tx_nombre.text())
                    oDivision.id_materia = str(self.Dialog.tx_id_materia.text())

                    query = 'INSERT OR REPLACE INTO tb_divisiones (id_division, division, id_materia) VALUES (?,?,?)'
                    crud = ClassCrud().Add(oDivision.DivisionToList(), query)

                    self.closeForm()
                else:
                    oDivision.id_division = int(self.Dialog.tx_codigo.text())
                    oDivision.division = str(self.Dialog.tx_nombre.text())
                    oDivision.id_materia = str(self.Dialog.tx_id_materia.text())

                    row = (oDivision.division, oDivision.id_materia,
                           oDivision.id_division)
                    query = 'UPDATE tb_divisiones SET division = ?, id_materia = ? WHERE id_division = ?'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos obligatorios", "Division")
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Division")

    def closeForm(self):
        self.QDialog.close()

    def searchMateriaWithId(self):
        try:
            if str(self.Dialog.tx_id_materia.text()) == "":
                self.Dialog.lb_id_materia.setText("")
            else:
                id = self.Dialog.tx_id_materia.text()
                query = "SELECT materia FROM tb_materias WHERE id_materia = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_id_materia.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_id_materia.text() == " None"):
                    self.Dialog.lb_id_materia.setText("")
        except Exception as e:
            print(e)

    def openFormSearchId(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Materias()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_id_materia)
        ventana.exec_()
