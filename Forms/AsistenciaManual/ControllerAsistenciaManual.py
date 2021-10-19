import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom
import datetime
import time

from Class.Crud import ClassCrud
from Models.Clase import ModelClase
from Models.Asistencia import ModelAsistencia

from Forms.Division.Division import Ui_Divisiones
from Forms.Profesor.Profesores import Ui_Profesores


import sqlite3


class ControllerAsistenciaManual(object):
    def __init__(self, Dialog, QDialog):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.validation()

        self.Dialog.tx_codigo_division.textChanged.connect(
            lambda: self.searchDivisionWithId())
        self.Dialog.tx_dni_profesor.textChanged.connect(
            lambda: self.searchProfesorWithId())

        self.Dialog.Bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.Bt_cancelar.clicked.connect(lambda: self.closeForm())
        self.Dialog.bt_division.clicked.connect(
            lambda: self.openFormSearchIdDivision())
        self.Dialog.bt_profesor.clicked.connect(
            lambda: self.openFormSearchDniProfesor())
        self.Dialog.tx_codigo_division.setFocus(True)

        self.Dialog.tx_entrada.setEnabled(False)
        self.Dialog.tx_salida.setEnabled(False)
        self.Dialog.tx_tardanza.setEnabled(True)

        self.Dialog.tx_entrada.setTime(QtCore.QTime(0, 0))
        self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))

        self.Dialog.tx_tardanza.stateChanged.connect(
            lambda: self.setEnabledEntradaSalida())

        try:
            self.calculateDelayAndClass(None, None)
        except:
            pass
    #########################################################################################

    def validation(self):
        self.onlyInt = QtGui.QIntValidator()
        self.Dialog.tx_dni_profesor.setValidator(self.onlyInt)
        self.Dialog.tx_codigo_division.setValidator(self.onlyInt)

    def validationData(self):
        if (self.Dialog.lb_division.text() != "" and self.Dialog.lb_profesor.text() != ""
                and self.Dialog.tx_entrada.text() != "" and self.Dialog.tx_salida.text() != ""):

            if(self.Dialog.bt_lunes.isChecked() == False and self.Dialog.bt_martes.isChecked() == False and
                    self.Dialog.bt_miercoles.isChecked() == False and self.Dialog.bt_jueves.isChecked() == False and
                    self.Dialog.bt_viernes.isChecked() == False and self.Dialog.bt_sabado.isChecked() == False):
                return False
            else:
                return True
        else:
            return False

    def getData(self):
        query = "select * from tb_clases WHERE id_clase ="
        crud = ClassCrud()
        result = crud.GetWithId(query, self.id_clase)
        self.Dialog.tx_codigo_division.setText(str(result[1]))
        self.Dialog.tx_dni_profesor.setText(str(result[2]))

        timeEntrada = QtCore.QTime(
            int((result[3])[0:2]), int((result[3])[3:5]))
        timeSalida = QtCore.QTime(int((result[4])[0:2]), int((result[4])[3:5]))

        self.Dialog.tx_entrada.setTime(timeEntrada)
        self.Dialog.tx_salida.setTime(timeSalida)

        if(result[5] == "Lunes"):
            self.Dialog.bt_lunes.setChecked(True)
        elif(result[5] == "Martes"):
            self.Dialog.bt_martes.setChecked(True)
        elif(result[5] == "Miercoles"):
            self.Dialog.bt_miercoles.setChecked(True)
        elif(result[5] == "Jueves"):
            self.Dialog.bt_jueves.setChecked(True)
        elif(result[5] == "Viernes"):
            self.Dialog.bt_viernes.setChecked(True)
        elif(result[5] == "Sábado"):
            self.Dialog.bt_sabado.setChecked(True)

        crud.connection.close()

    def saveRegister(self):
        self.saveAssistance(self.Dialog.tx_codigo_division.text(),
                            self.Dialog.tx_dni_profesor.text())

    def closeForm(self):
        self.QDialog.close()

    def searchDivisionWithId(self):
        try:
            if str(self.Dialog.tx_codigo_division.text()) == "":
                self.Dialog.lb_division.setText("")
            else:
                id = self.Dialog.tx_codigo_division.text()
                query = "SELECT division FROM tb_divisiones WHERE id_division = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_division.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_division.text() == " None"):
                    self.Dialog.lb_division.setText("")

                try:
                    self.calculateDelayAndClass(
                        self.Dialog.tx_codigo_division.text(), self.Dialog.tx_dni_profesor.text())
                except:
                    pass

        except Exception as e:
            print(e)

    def searchProfesorWithId(self):
        try:
            if str(self.Dialog.tx_dni_profesor.text()) == "":
                self.Dialog.lb_profesor.setText("")
            else:
                id = self.Dialog.tx_dni_profesor.text()
                query = "SELECT apellido, nombre FROM tb_profesores WHERE dni_profesor = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_profesor.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_profesor.text() == " None"):
                    self.Dialog.lb_profesor.setText("")

                try:
                    self.calculateDelayAndClass(
                        self.Dialog.tx_codigo_division.text(), self.Dialog.tx_dni_profesor.text())
                except:
                    pass
        except Exception as e:
            print(e)

    def openFormSearchIdDivision(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Divisiones()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_codigo_division)
        ventana.exec_()

    def openFormSearchDniProfesor(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Profesores()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_dni_profesor)
        ventana.exec_()

    def calculateDelayAndClass(self, id_division, dni_profesor):
        dia = self.getCurrentDay()
        query = "SELECT COUNT (id_clase) FROM tb_clases WHERE dni_profesor = " + dni_profesor + \
            " AND id_division = " + id_division + " AND dia = " + "'" + dia + "'"
        print(query)

        result = ClassCrud().GetWithIds(query)

        if (result[0] == 0 and self.Dialog.tx_tardanza.isChecked() == False):
            win32api.MessageBox(
                0, "No se encuentra una clase válida para la división y el profesor seleccionado, verifique lo datos ingresados o establezca que se trata de una clase de recuperación", "Asistencia manual")
            self.Dialog.Bt_guardar.setEnabled(False)
            self.Dialog.tx_tardanza.setEnabled(True)
            self.Dialog.tx_entrada.setTime(QtCore.QTime(0, 0))
            self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))

            return
        elif(result[0] == 0 and self.Dialog.tx_tardanza.isChecked() == True):
            self.Dialog.Bt_guardar.setEnabled(True)
            return
        else:
            self.Dialog.Bt_guardar.setEnabled(True)

        hora = datetime.datetime.now()
        hora = hora.strftime("%H:%M:%S")
        hora = QtCore.QTime(int((hora)[0:2]), int((hora)[3:5]))

        query3 = "SELECT * FROM tb_asistencias WHERE dni_profesor = " + \
            dni_profesor + " AND estado != 'Ausencia' AND estado != 'Recuperación' ORDER BY id_asistencia DESC LIMIT 1;"
        getLastState = ClassCrud().GetWithIds(query3)

        if(getLastState != None):
            try:
                print(getLastState)
                if(getLastState[7] == "Dentro del instituto" or getLastState[7] == "Dentro del instituto (recuperación)"):
                    self.Dialog.tx_salida.setTime(hora)
                    self.Dialog.tx_entrada.setTime(QtCore.QTime(0, 0))
                    self.Dialog.tx_tardanza.setEnabled(False)

                elif(getLastState[7] == "Fuera del instituto" or getLastState[7] == "Fuera del instituto (recuperación)"):
                    self.Dialog.tx_entrada.setTime(hora)
                    self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))
                    self.Dialog.tx_tardanza.setEnabled(True)

                else:
                    self.Dialog.tx_entrada.setTime(hora)
                    self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))
                    self.Dialog.tx_tardanza.setEnabled(True)

            except Exception as e:
                self.Dialog.tx_entrada.setTime(hora)
                self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))
                self.Dialog.tx_tardanza.setEnabled(True)
        else:
            self.Dialog.tx_entrada.setTime(hora)
            self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))
            self.Dialog.tx_tardanza.setEnabled(True)

    def saveAssistance(self, id_division, dni_profesor, dia="Martes"):
        query2 = ""

        if(self.Dialog.tx_tardanza.isChecked() == True):
            query2 = "SELECT entrada, salida, id_clase FROM tb_clases WHERE dni_profesor = " + \
                dni_profesor + " AND id_division = " + \
                id_division
        else:
            query2 = "SELECT entrada, salida, id_clase FROM tb_clases WHERE dni_profesor = " + \
                dni_profesor + " AND id_division = " + \
                id_division + " AND dia = " + "'" + dia + "'"

        currentClass = ClassCrud().GetWithIds(query2)

        if(currentClass == None):
            win32api.MessageBox(
                0, "El profesor no tiene de alta una clase válida para esta división y no se puede generar una asistencia.", "Asistencia manual")
            return

        queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
        sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

        oAsistencia = ModelAsistencia()
        oAsistencia.dni_profesor = dni_profesor
        oAsistencia.fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        oAsistencia.id_sede = int(sedeCicloDefault[0])
        oAsistencia.id_ciclo = int(sedeCicloDefault[1])
        oAsistencia.observacion = self.Dialog.tx_observacion.text()
        oAsistencia.id_clase = int(currentClass[2])

        ########################### CALCULAR TARDANZA #########################

        hora = datetime.datetime.now()
        hora = hora.strftime("%H:%M:%S")
        hora = datetime.datetime.strptime(hora, '%H:%M:%S')

        hora_entrada = currentClass[0] + ":00"
        hora_entrada = datetime.datetime.strptime(hora_entrada, '%H:%M:%S')

        hora_salida = currentClass[1] + ":00"
        hora_salida = datetime.datetime.strptime(hora_salida, '%H:%M:%S')

        tardanza = hora - hora_entrada
        restante = hora_salida - hora

        tardanzaPositiva = datetime.timedelta(hours=0, minutes=0, seconds=0)
        restantePositivo = datetime.timedelta(hours=0, minutes=0, seconds=0)

        if(tardanza > tardanzaPositiva and self.Dialog.tx_salida.text() == "00:00"):
            print("Si")
            tardanza = str(tardanza)
            tardanza = datetime.datetime.strptime(tardanza, '%H:%M:%S')
            print(str(tardanza))
            oAsistencia.tardanza = tardanza.strftime("%H:%M:%S")
        else:
            print("No")
            oAsistencia.tardanza = ""

        print(str(restante))
        print(str(restantePositivo))

        if(restante > restantePositivo and self.Dialog.tx_entrada.text() == "00:00"):
            print("Si restante")
            restante = str(restante)
            restante = datetime.datetime.strptime(restante, '%H:%M:%S')
            print(str(restante))
            oAsistencia.restante = restante.strftime("%H:%M:%S")
        else:
            print("No restante")
            oAsistencia.restante = ""

        ########################### CALCULAR SI ES ENTRADA O SALIDA #########################

        query3 = "SELECT * FROM tb_asistencias WHERE dni_profesor = " + \
            dni_profesor + " AND estado != 'Ausencia' AND estado != 'Recuperación' ORDER BY id_asistencia DESC LIMIT 1;"
        getLastState = ClassCrud().GetWithIds(query3)

        print(self.Dialog.tx_tardanza.checkState())
        if(self.Dialog.tx_tardanza.isChecked() == True):
            oAsistencia.hora_entrada = str(self.Dialog.tx_entrada.text())
            oAsistencia.hora_salida = str(self.Dialog.tx_salida.text())
            oAsistencia.estado = "Recuperación"
            oAsistencia.tardanza = "No aplica"
            oAsistencia.restante = "No aplica"

            self.generateAsitance(oAsistencia)
        else:
            try:
                print(getLastState[7])
                if(getLastState[7] == "Dentro del instituto"):
                    oAsistencia.estado = "Fuera del instituto"
                    oAsistencia.hora_salida = hora.strftime("%H:%M:%S")
                    print("entro")
                    try:
                        self.defineAssistanceClassProfessor(
                            id_division, dni_profesor)
                    except Exception as e:
                        print(e)
                elif(getLastState[7] == "Fuera del instituto" and self.Dialog.tx_tardanza.checkState() == False):
                    oAsistencia.estado = "Dentro del instituto"
                    oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")
                    self.generateAsitance(oAsistencia)
                else:
                    if(bool(self.Dialog.tx_tardanza.checkState()) == True):
                        oAsistencia.estado = "Dentro del instituto (recuperación)"
                        oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")
                        oAsistencia.tardanza = "No aplica"
                        oAsistencia.restante = "No aplica"
                    else:
                        print(getLastState[7])
                        print(bool(self.Dialog.tx_tardanza.checkState()))
                        oAsistencia.estado = "Dentro del instituto"
                        oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")

            except Exception as e:
                oAsistencia.estado = "Dentro del instituto"
                oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")

                self.generateAsitance(oAsistencia)
                print(e)

        ##############################################
        #                   return
        ##############################################

        # list = oAsistencia.AsistenciaToList()
        # for x in list:
        #     print(x)

        # queryAdd = 'INSERT OR REPLACE INTO tb_asistencias (dni_profesor, hora_entrada, hora_salida, tardanza, restante, fecha, estado, id_sede, id_ciclo, observacion, id_clase) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        # crud = ClassCrud().Add(oAsistencia.AsistenciaToList(), queryAdd)

        self.closeForm()

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

    def createMessageAlert(self, faltante):
        message = "Todavia faltan " + faltante + ""

        result = win32api.MessageBox(
            0, message, "Asistencias", 4)
        # 6 = Si
        # 7 = no
        if (result == 6):
            print("Hola")

    def defineAssistanceClassProfessor(self, id_division, dni_profesor):
        dia = self.getCurrentDay()
        queryClass = "SELECT Count(id_clase) FROM tb_clases WHERE dni_profesor =" + dni_profesor + " AND dia = '"+ dia + "'"
        countClass = ClassCrud().GetWithIds(queryClass)
        print(countClass[0])

        if(countClass[0] > 0):
            hora = datetime.datetime.now()
            hora = hora.strftime("%H:%M:%S")
            hora = datetime.datetime.strptime(hora, '%H:%M:%S')

            print(hora.strftime("%H:%M"))
            queryCurrentTodayClass = "SELECT * FROM tb_clases WHERE dni_profesor = " + dni_profesor + \
                " AND entrada <= " + "'" + \
                hora.strftime("%H:%M") + "' AND dia = '" + dia +"' order by salida asc"
            currentTodayClass = ClassCrud().Read(queryCurrentTodayClass).fetchall()
            queryGetTodayAsistanceProfessor = "SELECT id_clase, estado FROM tb_asistencias WHERE dni_profesor = " + dni_profesor
            getTodayAsistanceProfessor = ClassCrud().Read(
                queryGetTodayAsistanceProfessor).fetchall()
            print("//////////////////////////////")
            counter = 0
            for i in currentTodayClass:
                print(i[0])
                print(getTodayAsistanceProfessor[0])
                print(type(i[0]))
                print(type(getTodayAsistanceProfessor[0]))

                countAssitance = 0

                for j in getTodayAsistanceProfessor:
                    if(j[0] == i[0] and j[1] != 'Dentro del instituto'):
                        countAssitance = countAssitance + j.count(i[0])

                if(countAssitance == 0):
                    print("Esta clase no tiene asistencia")

                    querySelectIdClaseAssistanceToday = "Select id_clase from tb_asistencias where dni_profesor == " + \
                        dni_profesor + " and estado != 'Dentro del instituto'"
                    selectIdClaseAssistanceToday = ClassCrud().Read(
                        querySelectIdClaseAssistanceToday).fetchall()

                    oAsistencia = ModelAsistencia()

                    queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
                    sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

                    queryLastClass = "SELECT id_clase, salida FROM tb_clases WHERE dni_profesor = " + dni_profesor + \
                        " AND entrada <= " + "'" + \
                        hora.strftime("%H:%M") + "'" + " AND dia = '" + dia + "'"

                    try:
                        for f in selectIdClaseAssistanceToday:
                            queryLastClass += " AND id_clase != " + \
                                str(f[0]) + " "
                            print(queryLastClass)

                        queryLastClass += " order by salida  DESC limit 1"
                        print(queryLastClass)

                        LastClas = ClassCrud().GetWithIds(queryLastClass)
                    except Exception as e:
                        print(e)

                    hora_entrada = i[3] + ":00"
                    hora_entrada = datetime.datetime.strptime(
                        hora_entrada, '%H:%M:%S')

                    hora_salida = i[4] + ":00"
                    hora_salida = datetime.datetime.strptime(
                        hora_salida, '%H:%M:%S')

                    tardanza = hora - hora_entrada
                    restante = hora_salida - hora

                    tardanzaPositiva = datetime.timedelta(
                        hours=0, minutes=0, seconds=0)
                    restantePositivo = datetime.timedelta(
                        hours=0, minutes=0, seconds=0)

                    oAsistencia.dni_profesor = dni_profesor
                    oAsistencia.fecha = datetime.datetime.now().strftime("%d-%m-%Y")
                    oAsistencia.id_sede = int(sedeCicloDefault[0])
                    oAsistencia.id_ciclo = int(sedeCicloDefault[1])
                    oAsistencia.observacion = self.Dialog.tx_observacion.text()
                    oAsistencia.id_clase = int(i[0])

                    print(oAsistencia.id_clase)
                    print(LastClas[0])
                    print(type(oAsistencia.id_clase))
                    print(type(LastClas[0]))

                    if(oAsistencia.id_clase != LastClas[0]):
                        print("Diferente")
                        oAsistencia.estado = "Dentro del instituto"
                        oAsistencia.hora_entrada = i[3]
                        oAsistencia.hora_salida = i[4]
                    else:
                        print("Igual")
                        oAsistencia.estado = "Fuera del instituto"
                        oAsistencia.hora_entrada = ""
                        oAsistencia.hora_salida = hora.strftime("%H:%M:%S")

                        if(restante > restantePositivo):
                            print("Si restante")
                            restante = str(restante)
                            restante = datetime.datetime.strptime(
                                restante, '%H:%M:%S')
                            print(str(restante))
                            oAsistencia.restante = restante.strftime(
                                "%H:%M:%S")
                        else:
                            print("No restante")
                            oAsistencia.restante = ""

                    list = oAsistencia.AsistenciaToList()
                    for x in list:
                        print(x)

                    self.generateAsitance(oAsistencia)
                    # Error, no hay asistencia para esa clase, entonces hago logica para marcar las necesarias hasta el horario actual

            # print(str(counter))

    def generateAsitance(self, oAsistencia):
        list = oAsistencia.AsistenciaToList()
        # for x in list:
        #     print(x)

        queryAdd = 'INSERT OR REPLACE INTO tb_asistencias (dni_profesor, hora_entrada, hora_salida, tardanza, restante, fecha, estado, id_sede, id_ciclo, observacion, id_clase) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        crud = ClassCrud().Add(oAsistencia.AsistenciaToList(), queryAdd)

    def setEnabledEntradaSalida(self):
        if(self.Dialog.tx_tardanza.isChecked() == True):
            self.Dialog.tx_entrada.setEnabled(True)
            self.Dialog.tx_salida.setEnabled(True)

            self.Dialog.tx_entrada.setTime(QtCore.QTime(0, 0))
            self.Dialog.tx_salida.setTime(QtCore.QTime(0, 0))

            try:
                self.calculateDelayAndClass(
                    self.Dialog.tx_codigo_division.text(), self.Dialog.tx_dni_profesor.text())
            except:
                pass
        else:
            self.Dialog.tx_entrada.setEnabled(False)
            self.Dialog.tx_salida.setEnabled(False)

            try:
                self.calculateDelayAndClass(
                    self.Dialog.tx_codigo_division.text(), self.Dialog.tx_dni_profesor.text())
            except:
                pass