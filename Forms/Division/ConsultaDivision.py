# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ConsultaDivision.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConsultaDivision(object):
    def setupUi(self, Dialog, modificar, id_division):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(552, 213)
        Dialog.setMinimumSize(QtCore.QSize(552, 213))
        Dialog.setMaximumSize(QtCore.QSize(552, 213))
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setModal(True)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.tx_nombre = QtWidgets.QLineEdit(Dialog)
        self.tx_nombre.setGeometry(QtCore.QRect(110, 60, 411, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_nombre.setFont(font)
        self.tx_nombre.setObjectName("tx_nombre")
        self.bt_id_materia = QtWidgets.QPushButton(Dialog)
        self.bt_id_materia.setGeometry(QtCore.QRect(220, 100, 20, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_id_materia.setFont(font)
        self.bt_id_materia.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 16pt \"MS Shell Dlg 2\";")
        self.bt_id_materia.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("lupa.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_id_materia.setIcon(icon)
        self.bt_id_materia.setFlat(False)
        self.bt_id_materia.setObjectName("bt_id_materia")
        self.tx_codigo = QtWidgets.QLineEdit(Dialog)
        self.tx_codigo.setGeometry(QtCore.QRect(110, 20, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_codigo.setFont(font)
        self.tx_codigo.setObjectName("tx_codigo")
        self.tx_id_materia = QtWidgets.QLineEdit(Dialog)
        self.tx_id_materia.setGeometry(QtCore.QRect(110, 100, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        self.tx_id_materia.setFont(font)
        self.tx_id_materia.setObjectName("tx_id_materia")
        self.lb_id_materia = QtWidgets.QLabel(Dialog)
        self.lb_id_materia.setGeometry(QtCore.QRect(240, 100, 581, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.lb_id_materia.setFont(font)
        self.lb_id_materia.setText("")
        self.lb_id_materia.setObjectName("lb_id_materia")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 150, 511, 41))
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
        Dialog.setTabOrder(self.tx_codigo, self.tx_nombre)
        Dialog.setTabOrder(self.tx_nombre, self.tx_id_materia)
        Dialog.setTabOrder(self.tx_id_materia, self.bt_id_materia)

        from Forms.Division.ControllerConsultaDivision import ControllerConsultaDivision
        controller = ControllerConsultaDivision(self, Dialog, modificar, id_division)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "División"))
        self.label_2.setText(_translate("Dialog", "División"))
        self.label.setText(_translate("Dialog", "Código"))
        self.label_3.setText(_translate("Dialog", "Materia"))
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
