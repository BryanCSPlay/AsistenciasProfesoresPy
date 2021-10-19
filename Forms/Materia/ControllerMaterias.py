from PyQt5 import QtCore, QtGui, QtWidgets

import win32api
import win32com.client
import pythoncom
import sqlite3
from Class.Crud import ClassCrud
from Forms.Materia.ConsultaMateria import Ui_ConsultaMateria
from Models.MateriaCarrera import ModelMateriaCarrera


class ControllerMaterias(object):
    def __init__(self, Dialog, QDialog, selectRegister = False, ref_tx_id_materia = None, id_carrera = None, years = None):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.selectRegister = selectRegister
        self.ref_tx_id_materia = ref_tx_id_materia
        self.id_carrera = id_carrera
        self.years = years

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
        #header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.loadData()

    #########################################################################################

    def loadData(self, _query="select tb_materias.id_materia, tb_materias.materia from tb_materias"):
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
                        "select tb_materias.id_materia, tb_materias.materia from tb_materias WHERE id_materia=" + str(self.Dialog.tx_buscar.text()))

                elif self.Dialog.radioButton_materia.isChecked() == True:
                    self.loadData("select tb_materias.id_materia, tb_materias.materia from tb_materias WHERE materia LIKE" +
                                  "'" + str(self.Dialog.tx_buscar.text()) + "%'")
        except:
            return

    def maxId(self):
        connection = sqlite3.connect('db.s3db')

        try:
            maxId = connection.execute(
                "SELECT max(id_materia) FROM tb_materias").fetchone()
            connection.close()
            return str(int(maxId[0])+1)
        except:
            connection.close()
            return "1"

    def getId(self):
        try:
            index = self.Dialog.tableWidget.selectedIndexes()[0]
            id = int(self.Dialog.tableWidget.model().data(index))
            Data = (str(id))

            return Data
        except:
            win32api.MessageBox(0, "No se seleccionó ningún item", "Materias")
            return 0

    def eliminarRegistro(self):
        result = win32api.MessageBox(
            0, "¿Está seguro que desea eliminar el registro seleccionado?", "Materias", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            query = "DELETE FROM `tb_materias` WHERE id_materia = ?"
            ClassCrud().Delete((self.getId(),), query)
            self.loadData()
        return

    def openFormConsulta(self, _modificar):
        if (_modificar == False):
            ventana = QtWidgets.QDialog(self.QDialog)
            self.ui = Ui_ConsultaMateria()
            ventana.setWindowFlags(ventana.windowFlags(
            ) & ~QtCore.Qt.WindowContextHelpButtonHint)
            self.ui.setupUi(ventana, _modificar, self.maxId())
            ventana.exec_()
            self.loadData()

        else:
            if (self.getId() != 0):
                ventana = QtWidgets.QDialog(self.QDialog)
                self.ui = Ui_ConsultaMateria()
                ventana.setWindowFlags(ventana.windowFlags(
                ) & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.ui.setupUi(ventana, _modificar, self.getId())
                ventana.exec_()
                self.loadData()

    def getRegister(self):
        if(self.selectRegister == True and self.ref_tx_id_materia != None):
            self.ref_tx_id_materia.setText(str(self.getId()))
            self.QDialog.close()

        elif(self.selectRegister == True and self.id_carrera != None):
            oMateriaCarrera = ModelMateriaCarrera()

            oMateriaCarrera.id_materia = int(self.getId())
            oMateriaCarrera.id_carrera = str(self.id_carrera)
            oMateriaCarrera.years = int(self.years)

            query = 'INSERT OR REPLACE INTO tb_materias_carreras (id_materia, id_carrera, years) VALUES (?,?,?)'
            crud = ClassCrud().Add(oMateriaCarrera.MateriaCarreraToList(), query)

            self.QDialog.close()
