import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import win32api
import win32com.client
import pythoncom
import sqlite3

from Class.SendEmail import SendEmail

class ControllerEnviarQr(object):
    def __init__(self, Dialog, QDialog, dni):
        self.Dialog = Dialog
        self.QDialog = QDialog
        self.dni = dni

        self.load()

    def load(self):
        self.QDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.Dialog.bt_guardar.clicked.connect(lambda: self.sendQr())
        self.Dialog.bt_cancelar.clicked.connect(lambda: self.closeForm())

    def sendQr(self):
        oSendEmail = SendEmail(self.dni, self.Dialog.tx_email.text().strip())
        state = oSendEmail.sendEmail()

        if(state == "Ok"):
            win32api.MessageBox(
                0, "El E-Mail ha sido enviado con éxito", "Envío de código Qr")
            self.closeForm()
        else:
            win32api.MessageBox(
                0, "Algo ha fallado, por favor verifique el E-Mail", "Envío de código Qr")

    def closeForm(self):
        self.QDialog.close()
