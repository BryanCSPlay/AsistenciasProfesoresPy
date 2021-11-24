import win32api
import win32com.client
import pythoncom
import sys
from PyQt5 import uic, QtWidgets
import sqlite3
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from Forms.Carrera.Carreras import Ui_Carreras
from Forms.Materia.Materias import Ui_Materias
from Forms.CarreraMateria.CarrerasMaterias import Ui_MateriasCarrera
from Forms.Division.Division import Ui_Divisiones
from Forms.Profesor.Profesores import Ui_Profesores
from Forms.Clase.Clases import Ui_Clases
from Forms.Ciclo.Ciclos import Ui_Ciclos
from Forms.Sede.Sedes import Ui_Sedes
from Forms.AsistenciaManual.AsistenciaManual import Ui_AsistenciaManual
from Forms.AsistenciaManual.ConfigSedeCiclo import Ui_ConfigSedeCiclo
from Forms.Asistencia.Asistencias import Ui_Asistencias

from Class.Crud import ClassCrud
from Models.Asistencia import ModelAsistencia

import sys
from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

# Convert .ui to .py: pyuic5 segunda.ui -o segunda.py

qtCreatorFile = "MainForm.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Botones/Objects
        self.tx_buscar_asistencia.textChanged.connect(
            lambda: self.searchAsistencia())
        self.tx_buscar_hoy.textChanged.connect(lambda: self.searchHoy())

        self.Bt_marcar.clicked.connect(self.qrRead)
        self.bt_asistencia_manual.clicked.connect(
            self.abrirFormAssitenciaManual)
        self.bt_eliminar_asistencia.clicked.connect(self.eliminarRegistro)

        self.Bt_marcar.clicked.connect(self.qrRead)
        self.Bt_marcar_ausencia.clicked.connect(self.createAbsence)
        self.Bt_desmarcar_ausencia.clicked.connect(self.deleteAbsence)

        self.tx_date.dateChanged.connect(lambda: self.LoadData())
        self.tableWidget.doubleClicked.connect(self.doubleClicked_table)

        # CONECT EVENTOS MENU
        self.actionProfesores.triggered.connect(self.abrirFormProfesor)
        self.actionCarreras.triggered.connect(self.abrirFormCarreras)
        self.actionMaterias.triggered.connect(self.abrirFormMaterias)
        self.actionMateriasCarrera.triggered.connect(self.abrirMateriasCarrera)
        self.actionDivisiones.triggered.connect(self.abrirFormDivisiones)
        self.actionClases.triggered.connect(self.abrirFormClases)
        self.actionCiclos.triggered.connect(self.abrirFormCiclos)
        self.actionSedes.triggered.connect(self.abrirFormSedes)
        self.actionAsistencias.triggered.connect(self.abrirFormAsistencias)
        self.actionConfigurar_sede_y_ciclo.triggered.connect(
            self.abrirFormConfigSedeCiclo)

        # TextBoxs/Objects
        # self.tx_buscar_profesor.textChanged.connect(self.BuscarProfesor)

        self.tableWidget.setColumnHidden(0, True)

        self.tableWidget_hoy.setColumnHidden(0, True)
        self.tableWidget_hoy.setColumnHidden(1, True)
        self.tableWidget_hoy.setColumnHidden(9, True)
        self.tableWidget_hoy.setColumnHidden(10, True)
        self.tableWidget_hoy.setColumnHidden(13, True)

        header = self.tableWidget.horizontalHeader()
        header.setMinimumSectionSize(115)
        header.resizeSection(2, 150)
        header.resizeSection(3, 150)
        # header.resizeSection(7, 150)
        header.resizeSection(9, 180)
        header.resizeSection(10, 160)
        header.resizeSection(11, 160)
        header.resizeSection(12, 200)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        header2 = self.tableWidget_hoy.horizontalHeader()
        header2.setMinimumSectionSize(80)
        header2.resizeSection(4, 150)
        header2.resizeSection(5, 150)
        header2.resizeSection(6, 200)
        header2.resizeSection(7, 80)
        header2.resizeSection(8, 80)
        header2.resizeSection(11, 180)
        header2.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)

        #header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)

        self.tx_date.setDate(datetime.datetime.now())
        dateObject = self.tx_date.date().toPyDate()
        date = dateObject.strftime("%d-%m-%Y")

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    # FUNCIONES

    def mensaje(self):
        win32api.MessageBox(0, 'hello', 'title')

    def LoadData(self, _query="SELECT tb_asistencias.id_asistencia, tb_asistencias.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_asistencias.hora_entrada, tb_asistencias.hora_salida, tb_asistencias.tardanza, tb_asistencias.restante, tb_asistencias.fecha, tb_asistencias.estado, tb_sedes.sede, tb_ciclos.ciclo, tb_asistencias.observacion FROM tb_asistencias LEFT JOIN tb_profesores ON tb_asistencias.dni_profesor=tb_profesores.dni_profesor LEFT JOIN tb_sedes ON tb_asistencias.id_sede=tb_sedes.id_sede LEFT JOIN tb_ciclos ON tb_asistencias.id_ciclo=tb_ciclos.id_ciclo", filter=""):
        dateObject = self.tx_date.date().toPyDate()
        date = dateObject.strftime("%d-%m-%Y")

        crud = ClassCrud()
        if(filter == ""):
            result = crud.Read(_query + " WHERE fecha ==" +
                               "'" + str(date) + "'")
        else:
            result = crud.Read(_query + " WHERE fecha ==" +
                               "'" + str(date) + "' AND " + filter)

        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def LoadDataToday(self, _query="SELECT tb_clases.id_clase, tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_materias.materia, tb_clases.entrada, tb_clases.salida, tb_asistencias.tardanza, tb_asistencias.restante, tb_asistencias.estado, tb_clases.dia, tb_asistencias.id_asistencia FROM tb_clases LEFT JOIN tb_asistencias ON tb_clases.id_clase = tb_asistencias.id_clase LEFT JOIN tb_profesores ON tb_clases.dni_profesor = tb_profesores.dni_profesor LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_materias ON tb_divisiones.id_materia = tb_materias.id_materia WHERE (tb_clases.dia = ", filter=""):
        dia = self.getCurrentDay()
        date = datetime.datetime.now().strftime("%d-%m-%Y")

        fixQuery = "SELECT tb_clases.id_clase, tb_clases.id_division, tb_divisiones.division, tb_clases.dni_profesor, tb_profesores.apellido, tb_profesores.nombre, tb_materias.materia, tb_clases.entrada, tb_clases.salida, asistencias_hoy.tardanza, asistencias_hoy.restante, asistencias_hoy.estado, tb_clases.dia, asistencias_hoy.id_asistencia FROM tb_clases LEFT JOIN (SELECT * FROM tb_asistencias WHERE tb_asistencias.fecha = '" + \
            date + \
            "') asistencias_hoy ON tb_clases.id_clase = asistencias_hoy.id_clase LEFT JOIN tb_profesores ON tb_clases.dni_profesor = tb_profesores.dni_profesor LEFT JOIN tb_divisiones ON tb_clases.id_division = tb_divisiones.id_division LEFT JOIN tb_materias ON tb_divisiones.id_materia = tb_materias.id_materia WHERE (tb_clases.dia = "

        _query = fixQuery

        #print(_query)

        if(filter == ""):
            _query += "'" + dia + "' OR asistencias_hoy.estado = 'Recuperación')" + \
                " AND (asistencias_hoy.fecha is NULL OR asistencias_hoy.fecha = '" + \
                date + "')" + " ORDER by asistencias_hoy.id_asistencia"
        else:
            _query += "'" + dia + "' OR asistencias_hoy.estado = 'Recuperación')" + \
                " AND (asistencias_hoy.fecha is NULL OR asistencias_hoy.fecha = '" + \
                date + "') AND " + filter + " ORDER by asistencias_hoy.id_asistencia"

        crud = ClassCrud()
        result = crud.Read(_query)

        self.tableWidget_hoy.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.tableWidget_hoy.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_hoy.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        crud.DisconnectToDb()

    def LoadColorData(self):
        try:
            from Class.ColorsGrid import ClassColors
            classColors = ClassColors(self)
        except Exception as e:
            print(e)

    def ReadData(self):
        index = self.tableWidget.selectedIndexes()[0]
        id_us = int(self.tableWidget.model().data(index))
        #Datos = (str(id_us))

    def doubleClicked_table(self):
        index = self.tableWidget.selectedIndexes()[1]
        id_us = str(self.tableWidget.model().data(index))
        Datos = (str(id_us))
        #win32api.MessageBox(0, Datos, 'title')

    def BuscarProfesor(self):
        if self.radioButton_codigo.isChecked == True:
            self.LoadDataQuery(
                "select * from employees WHERE EmployeeId=" + str(self.tx_buscar_profesor.Text()))

    ################# ABRIR FORMS ##################
    def abrirFormProfesor(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Profesores()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormCarreras(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Carreras()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormMaterias(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Materias()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormDivisiones(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Divisiones()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormClases(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Clases()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirMateriasCarrera(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_MateriasCarrera()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormCiclos(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Ciclos()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormSedes(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Sedes()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        # self.ventana.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        # self.ventana.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormAsistencias(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_Asistencias()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ventana.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.ventana.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormConfigSedeCiclo(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_ConfigSedeCiclo()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def abrirFormAssitenciaManual(self):
        self.ventana = QtWidgets.QDialog(self)
        self.ui = Ui_AsistenciaManual()
        self.ventana.setWindowFlags(
            self.ventana.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(self.ventana)
        self.ventana.exec_()

        self.tx_date.setDate(datetime.datetime.now())
        dateObject = self.tx_date.date().toPyDate()
        date = dateObject.strftime("%d-%m-%Y")

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def close_window(self):
        self.close()

    def getId(self):
        try:
            self.tableWidget.setColumnHidden(0, False)

            index = self.tableWidget.selectedIndexes()[0]
            id = int(self.tableWidget.model().data(index))
            Data = (str(id))
            self.tableWidget.setColumnHidden(0, True)

            return Data
        except:
            win32api.MessageBox(
                0, "No se seleccionó ningún item", "Asistencias")
            return 0

    def eliminarRegistro(self):
        if(self.tx_date.date().toPyDate().strftime("%d-%m-%Y") == datetime.datetime.now().strftime("%d-%m-%Y")):
            result = win32api.MessageBox(
                0, "¿Está seguro que desea eliminar el registro seleccionado?", "Asistencias", 4)
            # 6 = Si
            # 7 = no
            if (result == 6):
                query = "DELETE FROM `tb_asistencias` WHERE id_asistencia = ?"
                ClassCrud().Delete((self.getId(),), query)

                self.tx_date.setDate(datetime.datetime.now())
                dateObject = self.tx_date.date().toPyDate()
                date = dateObject.strftime("%d-%m-%Y")
                self.LoadData()
                self.LoadDataToday()
                self.LoadColorData()
        else:
            win32api.MessageBox(
                0, "No se pueden eliminar asistencias antiguas", "Asistencias")

    def qrRead(self):
        from Class.ReadQr import ReadQrClass

        readQr = ReadQrClass(self.tableWidget, self.tableWidget_hoy, self.tx_date)
        #readQr.QrRecorder()

    def createAbsence(self):
        try:
            self.tableWidget_hoy.setColumnHidden(0, False)
            self.tableWidget_hoy.setColumnHidden(1, False)

            indexDni = self.tableWidget_hoy.selectedIndexes()[3]
            dni = self.tableWidget_hoy.model().data(indexDni)
            indexIdDivision = self.tableWidget_hoy.selectedIndexes()[1]
            idDivision = self.tableWidget_hoy.model().data(indexIdDivision)
            indexIdClase = self.tableWidget_hoy.selectedIndexes()[0]
            idClase = self.tableWidget_hoy.model().data(indexIdClase)
            print(str(dni))
            print(str(idDivision))
            print(str(idClase))

            self.tableWidget_hoy.setColumnHidden(0, True)
            self.tableWidget_hoy.setColumnHidden(1, True)

            queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
            sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

            oAsistencia = ModelAsistencia()
            oAsistencia.dni_profesor = dni
            oAsistencia.id_division = idDivision
            oAsistencia.id_clase = idClase
            oAsistencia.fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            oAsistencia.id_sede = int(sedeCicloDefault[0])
            oAsistencia.id_ciclo = int(sedeCicloDefault[1])
            oAsistencia.estado = "Ausencia"

            queryAdd = 'INSERT OR REPLACE INTO tb_asistencias (dni_profesor, hora_entrada, hora_salida, tardanza, restante, fecha, estado, id_sede, id_ciclo, observacion, id_clase) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
            crud = ClassCrud().Add(oAsistencia.AsistenciaToList(), queryAdd)

            self.LoadData()
            self.LoadDataToday()
            self.LoadColorData()
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "No se seleccionó ningún item", "Asistencias")

    def deleteAbsence(self):
        try:
            self.tableWidget_hoy.setColumnHidden(0, False)
            self.tableWidget_hoy.setColumnHidden(1, False)
            self.tableWidget_hoy.setColumnHidden(9, False)
            self.tableWidget_hoy.setColumnHidden(10, False)
            self.tableWidget_hoy.setColumnHidden(13, False)

            indexIdAsistencia = self.tableWidget_hoy.selectedIndexes()[13]
            idAsistencia = self.tableWidget_hoy.model().data(indexIdAsistencia)

            self.tableWidget_hoy.setColumnHidden(0, True)
            self.tableWidget_hoy.setColumnHidden(1, True)
            self.tableWidget_hoy.setColumnHidden(9, True)
            self.tableWidget_hoy.setColumnHidden(10, True)
            self.tableWidget_hoy.setColumnHidden(13, True)

            result = win32api.MessageBox(
                0, "¿Está seguro que desea desmarcar la ausencia del registro seleccionado?", "Asistencias", 4)
            # 6 = Si
            # 7 = no
            if (result == 6):
                query = "DELETE FROM `tb_asistencias` WHERE id_asistencia = ?"
                ClassCrud().Delete((idAsistencia,), query)

            self.LoadData()
            self.LoadDataToday()
            self.LoadColorData()
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "No se seleccionó ningún item", "Profesores")

    def getCurrentDay(self):
        day = time.strftime('%A')

        if(day == "Monday"):
            day = "Lunes"
        elif(day == "Tuesday"):
            day = "Martes"
        elif(day == "Wednesday"):
            day = "Miércoles"
        elif(day == "Thursday"):
            day = "Jueves"
        elif(day == "Friday"):
            day = "Viernes"
        elif(day == "Saturday"):
            day = "Sábado"
        elif(day == "Sunday"):
            day = "Domingo"

        return day

    def searchAsistencia(self):
        try:
            if str(self.tx_buscar_asistencia.text()) == "":
                self.LoadData()

            else:
                if self.radioButton_dni.isChecked() == True:
                    self.LoadData(filter="tb_asistencias.dni_profesor LIKE " +
                                  "'" + str(self.tx_buscar_asistencia.text()) + "%'")

                elif self.radioButton_apellido.isChecked() == True:
                    self.LoadData(filter="tb_profesores.apellido LIKE " +
                                  "'" + str(self.tx_buscar_asistencia.text()) + "%'")

                elif self.radioButton_nombre.isChecked() == True:
                    self.LoadData(filter="tb_profesores.nombre LIKE " +
                                  "'" + str(self.tx_buscar_asistencia.text()) + "%'")

                elif self.radioButton_entrada.isChecked() == True:
                    self.LoadData(filter="tb_asistencias.hora_entrada LIKE " +
                                  "'" + str(self.tx_buscar_asistencia.text()) + "%'")

                elif self.radioButton_salida.isChecked() == True:
                    self.LoadData(filter="tb_asistencias.hora_salida LIKE " +
                                  "'" + str(self.tx_buscar_asistencia.text()) + "%'")

        except Exception as e:
            print(e)
            return

    def searchHoy(self):
        try:
            if str(self.tx_buscar_hoy.text()) == "":
                self.LoadDataToday()
                self.LoadColorData()

            else:
                if self.radioButton_dni_hoy.isChecked() == True:
                    self.LoadDataToday(
                        filter="tb_clases.dni_profesor LIKE " + "'" + str(self.tx_buscar_hoy.text()) + "%'")

                elif self.radioButton_apellido_hoy.isChecked() == True:
                    self.LoadDataToday(
                        filter="tb_profesores.apellido LIKE " + "'" + str(self.tx_buscar_hoy.text()) + "%'")

                elif self.radioButton_nombre_hoy.isChecked() == True:
                    self.LoadDataToday(
                        filter="tb_profesores.nombre LIKE " + "'" + str(self.tx_buscar_hoy.text()) + "%'")

                elif self.radioButton_entrada_hoy.isChecked() == True:
                    self.LoadDataToday(
                        filter="tb_clases.entrada LIKE " + "'" + str(self.tx_buscar_hoy.text()) + "%'")

                elif self.radioButton_salida_hoy.isChecked() == True:
                    self.LoadDataToday(
                        filter="tb_clases.salida LIKE " + "'" + str(self.tx_buscar_hoy.text()) + "%'")

                self.LoadColorData()

        except Exception as e:
            print(e)
            return


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyApp()
        window.show()
        window.setWindowIcon(QtGui.QIcon('icon.png'))
    except Exception as e:
        win32api.MessageBox(
            0, str(e))

    sys.exit(app.exec_())
