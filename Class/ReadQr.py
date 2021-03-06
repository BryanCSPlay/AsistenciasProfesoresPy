import sys
from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
# pip install pyzbar (en consola)

from Class.Crud import ClassCrud
from Models.Asistencia import ModelAsistencia
import datetime

import win32api
import win32com.client
import pythoncom
import sys
from PyQt5 import uic, QtWidgets
import sqlite3


class ReadQrClass(object):
    def __init__(self, tableWidget, tableWidget_hoy, tx_date):
        self.tableWidget = tableWidget
        self.tableWidget_hoy = tableWidget_hoy
        self.tx_date = tx_date

        print("Inicio la cam")
        self.QrRecorder(self.tableWidget, self.tableWidget_hoy, self.tx_date)

    def getProfesor(self, _query="SELECT apellido FROM tb_profesores WHERE DNI =", id=None):
        crud = ClassCrud()
        result = crud.GetWithId(_query, id)

        crud.DisconnectToDb()

        return result

    def QrRecorder(self, tableWidget, tableWidget_hoy, tx_date):
        #img = cv2.imread('1.png')
        # Inicio la camara/WebCam
        
        cap = cv2.VideoCapture(0)

        profesor = ""
        currectRegister = ""
        timeLeave = ""

        # Determino el tamaño de la pantalla
        cap.set(3, 640)
        cap.set(4, 480)

        ######################################################################
        # Maquetado del perfil
        ######################################################################
        while True:

            success, img = cap.read()

            for barcode in decode(img):
                myData = ""
                try:
                    myData = barcode.data.decode('utf-8').encode('shift-jis').decode('utf-8')
                except:
                    myData = barcode.data.decode('utf-8')

                print(myData)
                
                profesor = self.getProfesor(
                    "SELECT apellido, dni_profesor FROM tb_profesores WHERE qr = '", str(myData) + "'")

                pts = np.array([barcode.polygon], np.int32)

                pts = pts.reshape((-1, 1, 2))

                cv2.polylines(img, [pts], True, (0, 255, 0), 5)
                pts2 = barcode.rect

                print(profesor)

                if(profesor != None):
                    cv2.putText(img, "Listo", (pts2[0], pts2[1] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 255, 0), 2)

                    cv2.putText(img, profesor[0], (10, 460), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 255, 0), 2)

                    dateNow = datetime.datetime.now()

                    if(currectRegister != profesor[0] or dateNow > new_time):
                        currectRegister = profesor[0]

                        date_and_time = datetime.datetime.now()
                        print(date_and_time)

                        time_change = datetime.timedelta(seconds=15)
                        new_time = date_and_time + time_change

                        print(new_time)

                        self.saveAssistance(profesor[1])

            cv2.imshow('Camara', img)

            # Cierro el exe
            keypress = cv2.waitKey(1) & 0xFF

            if keypress == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        ######################################################################

    def saveAssistance(self, dni_profesor):
        dia = self.getCurrentDay()
        date = datetime.datetime.now().strftime("%d-%m-%Y")

        querySelectIdClaseAssistanceToday = "Select id_clase from tb_asistencias where dni_profesor == " + \
            dni_profesor + " AND fecha = '" + date + "'"
        selectIdClaseAssistanceToday = ClassCrud().Read(
            querySelectIdClaseAssistanceToday).fetchall()

        print(querySelectIdClaseAssistanceToday)
        print(selectIdClaseAssistanceToday)
        query2 = "SELECT entrada, salida, id_clase, id_division FROM tb_clases WHERE dni_profesor = " + \
            dni_profesor + " AND dia = " + "'" + dia + "' "

        try:
            print(selectIdClaseAssistanceToday)
            for i in selectIdClaseAssistanceToday:
                query2 += "AND id_clase != " + str(i[0]) + " "
                print(query2)

            query2 += "order by entrada asc limit 1"
            print(query2)
            currentClass = ClassCrud().GetWithIds(query2)
            print(currentClass)

            if(currentClass == None):
                querySelectIdClaseAssistanceToday = "Select id_clase from tb_asistencias where dni_profesor == " + \
                    dni_profesor + " and estado != 'Dentro del instituto' AND fecha = '" + date + "'"
                selectIdClaseAssistanceToday = ClassCrud().Read(
                    querySelectIdClaseAssistanceToday).fetchall()

                print(querySelectIdClaseAssistanceToday)
                query2 = "SELECT entrada, salida, id_clase, id_division FROM tb_clases WHERE dni_profesor = " + \
                    dni_profesor + " AND dia = " + "'" + dia + "' "

                try:
                    print(selectIdClaseAssistanceToday)
                    for j in selectIdClaseAssistanceToday:
                        query2 += "AND id_clase != " + str(j[0]) + " "
                        print(query2)

                    query2 += "order by entrada asc limit 1"
                    print(query2)
                    currentClass = ClassCrud().GetWithIds(query2)
                    print(currentClass)
                except Exception as e:
                    print(e)
                    return
        except Exception as e:
            print(e)
            return

        if(currentClass == None):
            win32api.MessageBox(
                0, "El profesor no tiene de alta una clase válida para hoy y no se puede generar una asistencia.", "Asistencia QR")
            return

        queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
        sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

        oAsistencia = ModelAsistencia()
        oAsistencia.dni_profesor = dni_profesor
        oAsistencia.fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        oAsistencia.id_sede = int(sedeCicloDefault[0])
        oAsistencia.id_ciclo = int(sedeCicloDefault[1])
        #oAsistencia.observacion = self.Dialog.tx_observacion.text()
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

        if(tardanza > tardanzaPositiva):
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

        if(restante > restantePositivo):
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

        try:
            print(getLastState[7])
            if(getLastState[7] == "Dentro del instituto"):
                oAsistencia.estado = "Fuera del instituto"
                oAsistencia.hora_salida = hora.strftime("%H:%M:%S")
                oAsistencia.tardanza = ""
                print("entro")
                try:
                    self.defineAssistanceClassProfessor(
                        currentClass[3], dni_profesor)
                except Exception as e:
                    print(e)
            elif(getLastState[7] == "Fuera del instituto"):
                oAsistencia.estado = "Dentro del instituto"
                oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")
                oAsistencia.restante = ""
                self.generateAsitance(oAsistencia)
            else:
                print(getLastState[7])
                oAsistencia.estado = "Dentro del instituto"
                oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")
                oAsistencia.restante = ""

        except Exception as e:
            oAsistencia.estado = "Dentro del instituto"
            oAsistencia.hora_entrada = hora.strftime("%H:%M:%S")
            oAsistencia.restante = ""

            self.generateAsitance(oAsistencia)
            print(e)

        ##############################################
        # return
        ##############################################

        # list = oAsistencia.AsistenciaToList()
        # for x in list:
        #     print(x)

        # queryAdd = 'INSERT OR REPLACE INTO tb_asistencias (dni_profesor, hora_entrada, hora_salida, tardanza, restante, fecha, estado, id_sede, id_ciclo, observacion, id_clase) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        # crud = ClassCrud().Add(oAsistencia.AsistenciaToList(), queryAdd)

        self.LoadData()
        self.LoadDataToday()
        self.LoadColorData()

    def defineAssistanceClassProfessor(self, id_division, dni_profesor):
        dia = self.getCurrentDay()
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        queryClass = "SELECT Count(id_clase) FROM tb_clases WHERE dni_profesor =" + \
            dni_profesor
        countClass = ClassCrud().GetWithIds(queryClass)
        print(countClass[0])

        if(countClass[0] > 0):
            hora = datetime.datetime.now()
            hora = hora.strftime("%H:%M:%S")
            hora = datetime.datetime.strptime(hora, '%H:%M:%S')

            print(hora.strftime("%H:%M"))
            queryCurrentTodayClass = "SELECT * FROM tb_clases WHERE dni_profesor = " + \
                dni_profesor + " AND entrada <= " + \
                "'" + hora.strftime("%H:%M") + "' order by salida asc"
            currentTodayClass = ClassCrud().Read(queryCurrentTodayClass).fetchall()
            queryGetTodayAsistanceProfessor = "SELECT id_clase, estado FROM tb_asistencias WHERE dni_profesor = " + \
                dni_profesor + " AND fecha = '" + date + "'"
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
                        dni_profesor + " and estado != 'Dentro del instituto'" + \
                        " AND fecha = '" + date + "'"
                    selectIdClaseAssistanceToday = ClassCrud().Read(
                        querySelectIdClaseAssistanceToday).fetchall()

                    oAsistencia = ModelAsistencia()

                    queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
                    sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

                    queryLastClass = "SELECT id_clase, salida FROM tb_clases WHERE dni_profesor = " + dni_profesor + \
                        " AND entrada <= " + "'" + \
                        hora.strftime("%H:%M") + "'"

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
                    #oAsistencia.observacion = self.Dialog.tx_observacion.text()
                    oAsistencia.id_clase = int(i[0])

                    print(oAsistencia.id_clase)
                    print(LastClas[0])
                    print(type(oAsistencia.id_clase))
                    print(type(LastClas[0]))

                    #######
                    assistanceExistAsInside = False
                    if(oAsistencia.id_clase != LastClas[0]):
                        for j in getTodayAsistanceProfessor:
                            if(j[0] == i[0] and j[1] == 'Dentro del instituto'):
                                countAssitance = countAssitance + j.count(i[0])
                                assistanceExistAsInside = True
                                break
                    ##################

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

                    if(assistanceExistAsInside == True):
                        assistanceExistAsInside = False
                    else:
                        self.generateAsitance(oAsistencia)
                    # Error, no hay asistencia para esa clase, entonces hago logica para marcar las necesarias hasta el horario actual

    def generateAsitance(self, oAsistencia):
        list = oAsistencia.AsistenciaToList()
        # for x in list:
        #     print(x)

        queryAdd = 'INSERT OR REPLACE INTO tb_asistencias (dni_profesor, hora_entrada, hora_salida, tardanza, restante, fecha, estado, id_sede, id_ciclo, observacion, id_clase) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
        crud = ClassCrud().Add(oAsistencia.AsistenciaToList(), queryAdd)

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

        print(_query)

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