import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.Sede.ConsultaSede import Ui_ConsultaSede

import sqlite3

class ControllerSedes(object):
    def __init__(self, Dialog, QDialog, selectRegister=False, ref_tx_id_sede=None):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.selectRegister = selectRegister
        self.ref_tx_id_sede = ref_tx_id_sede

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_buscar.textChanged.connect(lambda: self.search())
        self.Dialog.bt_nuevo.clicked.connect(lambda: self.openFormConsulta(False))
        self.Dialog.bt_modificar.clicked.connect(lambda: self.openFormConsulta(True))
        self.Dialog.bt_eliminar.clicked.connect(lambda: self.eliminarRegistro())
        self.Dialog.tableWidgetSedes.doubleClicked.connect(
            lambda: self.getRegister())

        if(self.selectRegister == True):
            self.Dialog.bt_nuevo.setEnabled(False)
            self.Dialog.bt_modificar.setEnabled(False)
            self.Dialog.bt_eliminar.setEnabled(False)

        self.Dialog.tx_buscar.setFocus(True)
        self.loadData()

    #########################################################################################
    
    def loadData(self, _query="select * from tb_sedes"):
        crud = ClassCrud()
        result = crud.Read(_query)
        self.Dialog.tableWidgetSedes.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Dialog.tableWidgetSedes.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Dialog.tableWidgetSedes.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def search(self):
        try:
            if str(self.Dialog.tx_buscar.text()) == "":
                self.loadData()

            else:
                if self.Dialog.radioButton_codigo.isChecked() == True:
                    self.loadData(
                        "select * from tb_sedes WHERE id_sede =" + str(self.Dialog.tx_buscar.text()))

                else:
                    self.loadData("select * from tb_sedes WHERE sede LIKE" +
                                  "'" + str(self.Dialog.tx_buscar.text()) + "%'")
        except:
            return

    def maxId(self):
        connection = sqlite3.connect('db.s3db')

        try:
            maxId = connection.execute(
                "SELECT max(id_sede) FROM tb_sedes").fetchone()
            connection.close()
            return str(int(maxId[0])+1)
        except:
            connection.close()
            return "1"

    def getId(self):
        try:
            index = self.Dialog.tableWidgetSedes.selectedIndexes()[0]
            id = int(self.Dialog.tableWidgetSedes.model().data(index))
            Data = (str(id))

            return Data
        except:
            win32api.MessageBox(0, "No se seleccionó ningún item", "Sedes")
            return 0

    def getNombre(self):
        try:
            index = self.Dialog.tableWidgetSedes.selectedIndexes()[1]
            id = self.Dialog.tableWidgetSedes.model().data(index)
            Data = (" " + str(id))

            return Data
        except Exception as e:
            print(e)
            win32api.MessageBox(0, "No se seleccionó ningún item", "Sedes")
            return 0

    def eliminarRegistro(self):
        result = win32api.MessageBox(
            0, "¿Está seguro que desea eliminar el registro seleccionado?", "Sedes", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            query = "DELETE FROM `tb_sedes` WHERE id_sede = ?"
            ClassCrud().Delete((self.getId(),), query)
            self.loadData()
        return

    def openFormConsulta(self, modificar):
        if (modificar == False):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaSede()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, modificar, self.maxId())
            ventana.exec_()
            self.loadData()

        else:
            if (self.getId() != 0):
                ventana = QtWidgets.QDialog(self.QDialog)
                self.ui = Ui_ConsultaSede()
                ventana.setWindowFlags(ventana.windowFlags(
                ) & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.ui.setupUi(ventana, modificar, self.getId())
                ventana.exec_()
                self.loadData()

    def getRegister(self):
        if(self.selectRegister == True):
            self.ref_tx_id_sede.setText(str(self.getId()))
            self.QDialog.close()