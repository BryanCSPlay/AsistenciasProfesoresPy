import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.CarreraMateria.ConsultaYear import Ui_ConsultaYear

import sqlite3


class ControllerCarrerasMaterias(object):
    def __init__(self, Dialog, QDialog):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.id_carrera = 0
        return

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.loadDataCarreras()
        self.Dialog.tableWidgetCarreras.cellClicked.connect(
            lambda: self.changeSelectCarrera())
        # self.Dialog.tableWidgetCarreras.focus()
        self.Dialog.tx_buscar_carrera.textChanged.connect(lambda: self.searchCarrera())
        self.Dialog.tx_buscar_materia.textChanged.connect(lambda: self.searchMateria())

        self.Dialog.bt_nuevo.clicked.connect(lambda: self.agregarMateria())
        self.Dialog.bt_eliminar.clicked.connect(lambda: self.eliminarMateria())
        self.Dialog.tableWidgetMaterias.setRowCount(11)

        header = self.Dialog.tableWidgetMaterias.horizontalHeader()
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.Dialog.tableWidgetMaterias.setColumnHidden(0, True)


    def loadDataCarreras(self, _query="select * from tb_carreras"):
        # query = "select * from tb_carreras"
        crud = ClassCrud()
        result = crud.Read(_query)
        self.Dialog.tableWidgetCarreras.setRowCount(0)
        # print(result)
        for row_number, row_data in enumerate(result):
            self.Dialog.tableWidgetCarreras.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Dialog.tableWidgetCarreras.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def loadDataMaterias(self, _query="select * from tb_materias_carreras"):
        # query = "select * from tb_carreras"
        crud = ClassCrud()
        result = crud.Read(_query)
        self.Dialog.tableWidgetMaterias.setRowCount(0)
        # print(crud)
        for row_number, row_data in enumerate(result):
            self.Dialog.tableWidgetMaterias.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Dialog.tableWidgetMaterias.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def changeSelectCarrera(self):
        self.Dialog.tx_buscar_materia.setText("")
        self.loadDataMaterias(
            "select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia")

    def getIdCarrera(self):
        try:
            items = self.Dialog.tableWidgetCarreras.selectedItems()
            data = str(items[0].text())
            self.id_carrera = data

            return data
        except:
            win32api.MessageBox(0, "No se seleccionó ningún item", "Carreras")
            return 0

    def getIdMateria(self):
        try:
            self.Dialog.tableWidgetMaterias.setColumnHidden(0, False)
            items = self.Dialog.tableWidgetMaterias.selectedItems()
            data = str(items[0].text())
            self.id_carrera = data
            self.Dialog.tableWidgetMaterias.setColumnHidden(0, True)

            return data
        except:
            self.Dialog.tableWidgetMaterias.setColumnHidden(0, True)
            self.id_carrera = 0
            win32api.MessageBox(0, "No se seleccionó ningún item", "Materias")
            return 0

    def agregarMateria(self):
        existIdSelect = self.getIdCarrera()
        if(existIdSelect!=0):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaYear()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, self.id_carrera)
            ventana.exec_()
            self.loadDataMaterias(
                "select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia")

    def eliminarMateria(self):
        existIdSelect = self.getIdMateria()
        if(existIdSelect!=0):
            result = win32api.MessageBox(
                0, "¿Está seguro que desea eliminar el registro seleccionado?", "Materias por carrera", 4)
            # 6 = Si
            # 7 = no
            if (result == 6):
                query = "DELETE FROM `tb_materias_carreras` WHERE Id = ?"
                ClassCrud().Delete((existIdSelect,), query)
                self.loadDataMaterias(
                "select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia")


    def searchCarrera(self):
        try:
            if str(self.Dialog.tx_buscar_carrera.text()) == "":
                self.loadDataCarreras()

            else:
                if self.Dialog.radioButton_codigo_carrera.isChecked() == True:
                    self.loadDataCarreras(
                        "select * from tb_carreras WHERE id_carrera=" + str(self.Dialog.tx_buscar_carrera.text()))

                elif self.Dialog.radioButton_nombre_carrera.isChecked() == True:
                    self.loadDataCarreras("select * from tb_carreras WHERE carrera LIKE" +
                                  "'" + str(self.Dialog.tx_buscar_carrera.text()) + "%'")
        except:
            return


    def searchMateria(self):
        try:
            if str(self.Dialog.tx_buscar_materia.text()) == "":
                 self.loadDataMaterias(
            "select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia")
            else:
                if self.Dialog.radioButton_codigo_materia.isChecked() == True:
                    self.loadDataMaterias("select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia AND tb_materias_carreras.id_materia==" + str(self.Dialog.tx_buscar_materia.text()))

                elif self.Dialog.radioButton_nombre_materia.isChecked() == True:
                    self.loadDataMaterias("select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia AND tb_materias.materia LIKE" + "'" + str(self.Dialog.tx_buscar_materia.text()) + "%'")
        
                elif self.Dialog.radioButton_nombre_year.isChecked() == True:
                    self.loadDataMaterias("select tb_materias_carreras.Id, tb_materias_carreras.id_materia, tb_materias.materia, tb_materias_carreras.years from tb_materias_carreras, tb_materias WHERE tb_materias_carreras.id_carrera == " + self.getIdCarrera() + " AND tb_materias_carreras.id_materia == tb_materias.id_materia AND tb_materias_carreras.years ==" + str(self.Dialog.tx_buscar_materia.text()))
        
        
        except Exception as e:
            print(e)
            return