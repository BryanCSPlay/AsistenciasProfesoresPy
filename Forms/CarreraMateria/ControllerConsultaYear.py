import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.Materia.Materias import Ui_Materias

import sqlite3

class ControllerConsultaYear(object):
    def __init__(self, Dialog, QDialog, id_carrera):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.id_carrera = id_carrera

        self.load()

    def load(self):
        self.Dialog.Bt_siguiente.clicked.connect(lambda:self.openFormMaterias())
        self.Dialog.Bt_cancelar.clicked.connect(lambda:self.closeForm())

    def openFormMaterias(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Materias()
        ventana.setWindowFlags(ventana.windowFlags(
        ) & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, None, self.id_carrera, self.Dialog.tx_years.text())
        ventana.exec_()
        #print(str(self.id_carrera))
        self.closeForm()

    def closeForm(self):
        self.QDialog.close()

