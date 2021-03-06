# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ConsultaProfesor.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import win32api
import win32com.client

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConsultaProfesor(object):
    def setupUi(self, Dialog, modificar, id_profesor):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(754, 214)
        Dialog.setMinimumSize(QtCore.QSize(754, 214))
        Dialog.setMaximumSize(QtCore.QSize(754, 214))
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setModal(True)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tx_apellido = QtWidgets.QLineEdit(Dialog)
        self.tx_apellido.setGeometry(QtCore.QRect(110, 60, 401, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_apellido.setFont(font)
        self.tx_apellido.setText("")
        self.tx_apellido.setObjectName("tx_apellido")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tx_codigo = QtWidgets.QLineEdit(Dialog)
        self.tx_codigo.setGeometry(QtCore.QRect(110, 20, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_codigo.setFont(font)
        self.tx_codigo.setInputMask("")
        self.tx_codigo.setText("")
        self.tx_codigo.setObjectName("tx_codigo")
        self.tx_nombre = QtWidgets.QLineEdit(Dialog)
        self.tx_nombre.setGeometry(QtCore.QRect(110, 100, 401, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_nombre.setFont(font)
        self.tx_nombre.setText("")
        self.tx_nombre.setObjectName("tx_nombre")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tx_fn = QtWidgets.QDateEdit(Dialog)
        self.tx_fn.setGeometry(QtCore.QRect(390, 20, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_fn.setFont(font)
        self.tx_fn.setObjectName("tx_fn")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(230, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.tx_qr = QtWidgets.QLabel(Dialog)
        self.tx_qr.setGeometry(QtCore.QRect(550, 20, 171, 171))
        self.tx_qr.setText("")
        self.tx_qr.setObjectName("tx_qr")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 150, 501, 41))
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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.tx_codigo, self.tx_apellido)
        Dialog.setTabOrder(self.tx_apellido, self.tx_nombre)
        Dialog.setTabOrder(self.tx_nombre, self.tx_fn)
        
        from Forms.Profesor.ControllerConsultaProfesor import ControllerConsultaProfesor
        controller = ControllerConsultaProfesor(self, Dialog, modificar, id_profesor)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Profesor"))
        self.label_3.setText(_translate("Dialog", "Nombre"))
        self.label.setText(_translate("Dialog", "DNI"))
        self.label_2.setText(_translate("Dialog", "Apellido"))
        self.label_4.setText(_translate("Dialog", "Fecha de nacimiento"))
        self.bt_guardar.setText(_translate("Dialog", "Guardar"))
        self.bt_cancelar.setText(_translate("Dialog", "Cancelar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
