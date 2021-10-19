import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom

from Class.Crud import ClassCrud
from Forms.Clase.ConsultaClase import Ui_ConsultaClase

import sqlite3


class ControllerClases(object):
    def __init__(self, Dialog, QDialog, selectRegister=False):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.selectRegister = selectRegister

        self.customGrid()
        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_buscar.textChanged.connect(lambda: self.search())
        self.Dialog.bt_nuevo.clicked.connect(
            lambda: self.openFormConsulta(False))
        self.Dialog.bt_modificar.clicked.connect(
            lambda: self.openFormConsulta(True))
        self.Dialog.bt_eliminar.clicked.connect(
            lambda: self.eliminarRegistro())

        if(self.selectRegister == True):
            self.Dialog.bt_nuevo.setEnabled(False)
            self.Dialog.bt_modificar.setEnabled(False)
            self.Dialog.bt_eliminar.setEnabled(False)

        self.Dialog.tx_buscar.setFocus(True)
        self.loadData()

    def customGrid(self):
        header = self.Dialog.tableWidget.horizontalHeader()

        self.Dialog.tableWidget.setColumnHidden(0, True)
        self.Dialog.tableWidget.setColumnHidden(1, True)

        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

    #########################################################################################

    def loadData(self, _query="SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor = tb_profesores.dni_profesor"):
        # query = "select * from tb_carreras"
        crud = ClassCrud()
        result = crud.Read(_query)
        self.Dialog.tableWidget.setRowCount(0)
        # print(crud)
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
                if self.Dialog.radioButton_division.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_divisiones.division LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_dni.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_clases.dni_profesor LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_apellido.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_profesores.apellido LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_nombre.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_profesores.nombre LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_entrada.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_clases.entrada LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_salida.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_clases.salida LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

                elif self.Dialog.radioButton_dia.isChecked() == True:
                    self.loadData(
                        "SELECT tb_clases.id_clase,tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_clases.entrada,tb_clases.salida, tb_clases.dia FROM tb_clases LEFT JOIN tb_divisiones ON tb_clases.id_division == tb_divisiones.id_division LEFT JOIN tb_profesores ON tb_clases.dni_profesor == tb_profesores.dni_profesor WHERE tb_clases.dia LIKE " + "'" + str(self.Dialog.tx_buscar.text()) + "%'")

        except Exception as e:
            print(e)
            return

    def maxId(self):
        connection = sqlite3.connect('db.s3db')
        maxId = connection.execute(
            "select max(id_carrera) from tb_carreras").fetchone()
        connection.close()

        return str(int(maxId[0])+1)

    def getId(self):
        try:
            self.Dialog.tableWidget.setColumnHidden(0, False)

            index = self.Dialog.tableWidget.selectedIndexes()[0]
            id = int(self.Dialog.tableWidget.model().data(index))
            Data = (str(id))
            self.Dialog.tableWidget.setColumnHidden(0, True)

            return Data
        except:
            win32api.MessageBox(0, "No se seleccionó ningún item", "Carreras")
            return 0

    def eliminarRegistro(self):
        result = win32api.MessageBox(
            0, "¿Está seguro que desea eliminar el registro seleccionado?", "Carreras", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            query = "DELETE FROM `tb_clases` WHERE id_clase = ?"
            ClassCrud().Delete((self.getId(),), query)
            self.loadData()
        return

    def openFormConsulta(self, modificar):
        if (modificar == False):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaClase()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, modificar, "0")
            ventana.exec_()
            self.loadData()

        else:
            if (self.getId() != 0):
                ventana = QtWidgets.QDialog(self.QDialog)
                self.ui = Ui_ConsultaClase()
                ventana.setWindowFlags(ventana.windowFlags(
                ) & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.ui.setupUi(ventana, modificar, self.getId())
                ventana.exec_()
                self.loadData()
