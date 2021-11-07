# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\EnviarQr.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EnvioQr(object):
    def setupUi(self, EnvioQr, dni):
        EnvioQr.setObjectName("EnvioQr")
        EnvioQr.resize(426, 141)
        EnvioQr.setMinimumSize(QtCore.QSize(426, 141))
        EnvioQr.setMaximumSize(QtCore.QSize(426, 141))
        EnvioQr.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tx_email = QtWidgets.QLineEdit(EnvioQr)
        self.tx_email.setGeometry(QtCore.QRect(70, 30, 331, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_email.setFont(font)
        self.tx_email.setText("")
        self.tx_email.setObjectName("tx_email")
        self.horizontalLayoutWidget = QtWidgets.QWidget(EnvioQr)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 401, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bt_guardar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.bt_guardar.setMaximumSize(QtCore.QSize(161, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_guardar.setFont(font)
        self.bt_guardar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_guardar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.bt_guardar.setObjectName("bt_guardar")
        self.horizontalLayout.addWidget(self.bt_guardar)
        self.bt_cancelar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.bt_cancelar.setMaximumSize(QtCore.QSize(161, 41))
        self.bt_cancelar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_cancelar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.bt_cancelar.setObjectName("bt_cancelar")
        self.horizontalLayout.addWidget(self.bt_cancelar)
        self.label_2 = QtWidgets.QLabel(EnvioQr)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(EnvioQr)
        QtCore.QMetaObject.connectSlotsByName(EnvioQr)

        from Forms.Profesor.ControllerEnviarQr import ControllerEnviarQr
        controller = ControllerEnviarQr(self, EnvioQr, dni)

    def retranslateUi(self, EnvioQr):
        _translate = QtCore.QCoreApplication.translate
        EnvioQr.setWindowTitle(_translate("EnvioQr", "Enviar QR"))
        self.bt_guardar.setText(_translate("EnvioQr", "Enviar"))
        self.bt_cancelar.setText(_translate("EnvioQr", "Cancelar"))
        self.label_2.setText(_translate("EnvioQr", "E-Mail"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EnvioQr = QtWidgets.QDialog()
    ui = Ui_EnvioQr()
    ui.setupUi(EnvioQr)
    EnvioQr.show()
    sys.exit(app.exec_())
