import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.Carrera.ConsultaCarrera import Ui_ConsultaCarrera

import sqlite3

class ControllerCarreras(object):
    def __init__(self, Dialog, QDialog, selectRegister=False, ref_tx_id_carrera=None):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.selectRegister = selectRegister
        self.ref_tx_id_carrera = ref_tx_id_carrera

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_buscar_carrera.textChanged.connect(lambda: self.search())
        self.Dialog.bt_nuevo.clicked.connect(lambda: self.openFormConsulta(False))
        self.Dialog.bt_modificar.clicked.connect(lambda: self.openFormConsulta(True))
        self.Dialog.bt_eliminar.clicked.connect(lambda: self.eliminarRegistro())
        self.Dialog.tableWidgetCarrera.doubleClicked.connect(
            lambda: self.getRegister())

        if(self.selectRegister == True):
            self.Dialog.bt_nuevo.setEnabled(False)
            self.Dialog.bt_modificar.setEnabled(False)
            self.Dialog.bt_eliminar.setEnabled(False)

        self.Dialog.tx_buscar_carrera.setFocus(True)
        self.loadData()

    #########################################################################################
    
    def loadData(self, _query="select * from tb_carreras"):
        # query = "select * from tb_carreras"
        crud = ClassCrud()
        result = crud.Read(_query)
        self.Dialog.tableWidgetCarrera.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Dialog.tableWidgetCarrera.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Dialog.tableWidgetCarrera.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def search(self):
        try:
            if str(self.Dialog.tx_buscar_carrera.text()) == "":
                self.loadData()

            else:
                if self.Dialog.radioButton_codigo.isChecked() == True:
                    self.loadData(
                        "select * from tb_carreras WHERE id_carrera=" + str(self.Dialog.tx_buscar_carrera.text()))

                else:
                    self.loadData("select * from tb_carreras WHERE carrera LIKE" +
                                  "'" + str(self.Dialog.tx_buscar_carrera.text()) + "%'")
        except:
            return

    def maxId(self):
        connection = sqlite3.connect('db.s3db')
        maxId = connection.execute(
            "select max(id_carrera) from tb_carreras").fetchone()
        connection.close()

        return str(int(maxId[0])+1)

    def getId(self):
        try:
            index = self.Dialog.tableWidgetCarrera.selectedIndexes()[0]
            id = int(self.Dialog.tableWidgetCarrera.model().data(index))
            Data = (str(id))

            return Data
        except:
            win32api.MessageBox(0, "No se seleccionó ningún item", "Carreras")
            return 0

    def getNombre(self):
        try:
            index = self.Dialog.tableWidgetCarrera.selectedIndexes()[1]
            id = self.Dialog.tableWidgetCarrera.model().data(index)
            Data = (" " + str(id))

            return Data
        except Exception as e:
            print(e)
            win32api.MessageBox(0, "No se seleccionó ningún item", "Carreras")
            return 0

    def eliminarRegistro(self):
        result = win32api.MessageBox(
            0, "¿Está seguro que desea eliminar el registro seleccionado?", "Carreras", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            query = "DELETE FROM `tb_carreras` WHERE id_carrera = ?"
            ClassCrud().Delete((self.getId(),), query)
            self.loadData()
        return

    def openFormConsulta(self, modificar):
        if (modificar == False):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaCarrera()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, modificar, self.maxId())
            ventana.exec_()
            self.loadData()

        else:
            if (self.getId() != 0):
                ventana = QtWidgets.QDialog(self.QDialog)
                self.ui = Ui_ConsultaCarrera()
                ventana.setWindowFlags(ventana.windowFlags(
                ) & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.ui.setupUi(ventana, modificar, self.getId())
                ventana.exec_()
                self.loadData()

    def getRegister(self):
        if(self.selectRegister == True):
            self.ref_tx_id_carrera.setText(str(self.getId()))
            self.ventana.close()