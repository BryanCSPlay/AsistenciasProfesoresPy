from Forms.Sede.Sedes import Ui_Sedes
from Forms.Ciclo.Ciclos import Ui_Ciclos
from PyQt5 import QtCore, QtGui, QtWidgets
from Class.Crud import ClassCrud
import win32api
import win32com.client

class ControllerConfigSedeCiclo(object):
    def __init__(self, Dialog, QDialog):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))

        self.Dialog.tx_codigo_sede.textChanged.connect(
            lambda: self.searchSedeWithId())
        self.Dialog.tx_codigo_ciclo.textChanged.connect(
            lambda: self.searchCicloWithId())

        self.Dialog.Bt_guardar.clicked.connect(lambda: self.saveRegister())
        self.Dialog.Bt_cancelar.clicked.connect(lambda: self.closeForm())

        self.Dialog.bt_id_sede.clicked.connect(lambda: self.openFormSearchIdSede())
        self.Dialog.bt_id_ciclo.clicked.connect(lambda: self.openFormSearchIdCiclo())

        self.loadData()

    def loadData(self):
        queryConfig = "SELECT id_sede_default, id_ciclo_default FROM tb_configurations WHERE id = 1"
        sedeCicloDefault = ClassCrud().GetWithIds(queryConfig)

        self.Dialog.tx_codigo_sede.setText(str(sedeCicloDefault[0]))
        self.Dialog.tx_codigo_ciclo.setText(str(sedeCicloDefault[1]))

    def searchSedeWithId(self):
        try:
            if str(self.Dialog.tx_codigo_sede.text()) == "":
                self.Dialog.lb_id_sede.setText("")
            else:
                id = self.Dialog.tx_codigo_sede.text()
                query = "SELECT sede FROM tb_sedes WHERE id_sede = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_id_sede.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_id_sede.text() == " None"):
                    self.Dialog.lb_id_sede.setText("")
        except Exception as e:
            print(e)

    def searchCicloWithId(self):
        try:
            if str(self.Dialog.tx_codigo_ciclo.text()) == "":
                self.Dialog.lb_id_ciclo.setText("")
            else:
                id = self.Dialog.tx_codigo_ciclo.text()
                query = "SELECT ciclo FROM tb_ciclos WHERE id_ciclo = "
                result = ClassCrud().GetWithId(query, id)
                self.Dialog.lb_id_ciclo.setText(
                    " " + str(result).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
                if (self.Dialog.lb_id_ciclo.text() == " None"):
                    self.Dialog.lb_id_ciclo.setText("")
        except Exception as e:
            print(e)

    def openFormSearchIdSede(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Sedes()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_codigo_sede)
        ventana.exec_()
    
    def openFormSearchIdCiclo(self):
        ventana = QtWidgets.QDialog(self.QDialog)
        self.ui = Ui_Ciclos()
        ventana.setWindowFlags(ventana.windowFlags() & ~
                               QtCore.Qt.WindowContextHelpButtonHint)
        self.ui.setupUi(ventana, True, self.Dialog.tx_codigo_ciclo)
        ventana.exec_()

    def saveRegister(self):
        try:
            if(self.validationData() == True):
                try:
                    id_sede = int(self.Dialog.tx_codigo_sede.text())
                    id_ciclo = str(self.Dialog.tx_codigo_ciclo.text())

                    row = (id_sede, id_ciclo)
                    query = 'UPDATE tb_configurations SET id_sede_default = ?, id_ciclo_default = ? WHERE id = 1'
                    crud = ClassCrud().Update(row, query)

                    self.closeForm()
                except Exception as e:
                    print(e)
            else:
                win32api.MessageBox(
                    0, "Error, complete todos los campos", "Configuración")
        except Exception as e:
            print(e)
            win32api.MessageBox(
                0, "Error, no se ha podido guardar el registro", "Configuración")

    def closeForm(self):
        self.QDialog.close()

    def validationData(self):
        if (self.Dialog.lb_id_sede.text() != "" and self.Dialog.lb_id_ciclo.text() != ""):
            return True
        else:
            return False