import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.Profesor.ConsultaProfesor import Ui_ConsultaProfesor

import sqlite3

class ControllerProfesores(object):
    def __init__(self, Dialog, QDialog, selectRegister, ref_tx_dni_profesor):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.selectRegister = selectRegister
        self.ref_tx_dni_profesor = ref_tx_dni_profesor

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_buscar.textChanged.connect(lambda: self.search())
        self.Dialog.bt_nuevo.clicked.connect(lambda: self.openFormConsulta(False))
        self.Dialog.bt_modificar.clicked.connect(lambda: self.openFormConsulta(True))
        self.Dialog.bt_eliminar.clicked.connect(lambda: self.eliminarRegistro())
        self.Dialog.tableWidget.doubleClicked.connect(
            lambda: self.getRegister())

        self.Dialog.tx_buscar.setFocus(True)

        header = self.Dialog.tableWidget.horizontalHeader()
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.loadData()

    def loadData(self, _query="select tb_profesores.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_profesores.fn from tb_profesores"):
        # query = "select * from tb_carreras"
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
            if str(self.Dialog.tx_buscar.text()) == "":
                self.loadData()

            else:
                if self.Dialog.radioButton_codigo.isChecked() == True:
                    self.loadData(
                        "select tb_profesores.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_profesores.fn from tb_profesores WHERE dni_profesor LIKE" + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_apellido.isChecked() == True:
                    self.loadData("select tb_profesores.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_profesores.fn from tb_profesores WHERE apellido LIKE" +
                                  "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_nombre.isChecked() == True:
                    self.loadData("select tb_profesores.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_profesores.fn from tb_profesores WHERE nombre LIKE" +
                                  "'" + str(self.Dialog.tx_buscar.text()) + "%'")

        except:
            return

    def getId(self):
        try:
            index = self.Dialog.tableWidget.selectedIndexes()[0]
            id = int(self.Dialog.tableWidget.model().data(index))
            Data = (str(id))

            return Data
        except:
            win32api.MessageBox(
                0, "No se seleccionó ningún item", "Profesores")
            return 0

    def getNombre(self):
        try:
            index = self.Dialog.tableWidget.selectedIndexes()[1]
            id = self.Dialog.tableWidget.model().data(index)
            Data = (" " + str(id))

            return Data
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "No se seleccionó ningún item", "Profesores")
            return 0
        


    def eliminarRegistro(self):
        result = win32api.MessageBox(
            0, "¿Está seguro que desea eliminar el registro seleccionado?", "Profesores", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            query = "DELETE FROM `tb_profesores` WHERE dni_profesor = ?"
            ClassCrud().Delete((self.getId(),), query)
            self.loadData()
        return

    def openFormConsulta(self, _modificar):
        if (_modificar == False):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaProfesor()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, _modificar, "0")
            ventana.exec_()
            self.loadData()

        else:
            if (self.getId() != 0):
                ventana = QtWidgets.QDialog(self.QDialog)
                self.ui = Ui_ConsultaProfesor()
                ventana.setWindowFlags(ventana.windowFlags(
                ) & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.ui.setupUi(ventana, _modificar, self.getId())
                ventana.exec_()
                self.loadData()

    def getRegister(self):
        if(self.selectRegister == True):
            self.ref_tx_dni_profesor.setText(str(self.getId()))
            self.QDialog.close()