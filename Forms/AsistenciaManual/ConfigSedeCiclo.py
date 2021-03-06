# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ConfigSedeCiclo.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfigSedeCiclo(object):
    def setupUi(self, ConfigSedeCiclo):
        ConfigSedeCiclo.setObjectName("ConfigSedeCiclo")
        ConfigSedeCiclo.resize(542, 175)
        ConfigSedeCiclo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label = QtWidgets.QLabel(ConfigSedeCiclo)
        self.label.setGeometry(QtCore.QRect(30, 20, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tx_codigo_sede = QtWidgets.QLineEdit(ConfigSedeCiclo)
        self.tx_codigo_sede.setGeometry(QtCore.QRect(110, 20, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_codigo_sede.setFont(font)
        self.tx_codigo_sede.setInputMask("")
        self.tx_codigo_sede.setText("")
        self.tx_codigo_sede.setObjectName("tx_codigo_sede")
        self.tx_codigo_ciclo = QtWidgets.QLineEdit(ConfigSedeCiclo)
        self.tx_codigo_ciclo.setGeometry(QtCore.QRect(110, 60, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_codigo_ciclo.setFont(font)
        self.tx_codigo_ciclo.setObjectName("tx_codigo_ciclo")
        self.label_2 = QtWidgets.QLabel(ConfigSedeCiclo)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(ConfigSedeCiclo)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 110, 501, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Bt_guardar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Bt_guardar.setMaximumSize(QtCore.QSize(161, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Bt_guardar.setFont(font)
        self.Bt_guardar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Bt_guardar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.Bt_guardar.setObjectName("Bt_guardar")
        self.horizontalLayout.addWidget(self.Bt_guardar)
        self.Bt_cancelar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Bt_cancelar.setMaximumSize(QtCore.QSize(161, 41))
        self.Bt_cancelar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Bt_cancelar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.Bt_cancelar.setObjectName("Bt_cancelar")
        self.horizontalLayout.addWidget(self.Bt_cancelar)
        self.lb_id_ciclo = QtWidgets.QLabel(ConfigSedeCiclo)
        self.lb_id_ciclo.setGeometry(QtCore.QRect(240, 60, 581, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.lb_id_ciclo.setFont(font)
        self.lb_id_ciclo.setText("")
        self.lb_id_ciclo.setObjectName("lb_id_ciclo")
        self.bt_id_ciclo = QtWidgets.QPushButton(ConfigSedeCiclo)
        self.bt_id_ciclo.setGeometry(QtCore.QRect(220, 60, 20, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_id_ciclo.setFont(font)
        self.bt_id_ciclo.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 16pt \"MS Shell Dlg 2\";")
        self.bt_id_ciclo.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("lupa.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_id_ciclo.setIcon(icon)
        self.bt_id_ciclo.setFlat(False)
        self.bt_id_ciclo.setObjectName("bt_id_ciclo")
        self.lb_id_sede = QtWidgets.QLabel(ConfigSedeCiclo)
        self.lb_id_sede.setGeometry(QtCore.QRect(240, 20, 581, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.lb_id_sede.setFont(font)
        self.lb_id_sede.setText("")
        self.lb_id_sede.setObjectName("lb_id_sede")
        self.bt_id_sede = QtWidgets.QPushButton(ConfigSedeCiclo)
        self.bt_id_sede.setGeometry(QtCore.QRect(220, 20, 20, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_id_sede.setFont(font)
        self.bt_id_sede.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 16pt \"MS Shell Dlg 2\";")
        self.bt_id_sede.setText("")
        self.bt_id_sede.setIcon(icon)
        self.bt_id_sede.setFlat(False)
        self.bt_id_sede.setObjectName("bt_id_sede")

        self.retranslateUi(ConfigSedeCiclo)
        QtCore.QMetaObject.connectSlotsByName(ConfigSedeCiclo)

        from Forms.AsistenciaManual.ControllerConfigSedeCiclo import ControllerConfigSedeCiclo
        controller = ControllerConfigSedeCiclo(self, ConfigSedeCiclo)

    def retranslateUi(self, ConfigSedeCiclo):
        _translate = QtCore.QCoreApplication.translate
        ConfigSedeCiclo.setWindowTitle(_translate("ConfigSedeCiclo", "Sede y ciclo predefinido"))
        self.label.setText(_translate("ConfigSedeCiclo", "Cod. Sede"))
        self.label_2.setText(_translate("ConfigSedeCiclo", "Cod. Ciclo"))
        self.Bt_guardar.setText(_translate("ConfigSedeCiclo", "Guardar"))
        self.Bt_cancelar.setText(_translate("ConfigSedeCiclo", "Cancelar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigSedeCiclo = QtWidgets.QDialog()
    ui = Ui_ConfigSedeCiclo()
    ui.setupUi(ConfigSedeCiclo)
    ConfigSedeCiclo.show()
    sys.exit(app.exec_())
