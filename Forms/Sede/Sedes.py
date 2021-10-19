# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Sedes.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Sedes(object):
    def setupUi(self, Sedes, selectRegister = None, ref_tx_id_sede = None):
        Sedes.setObjectName("Sedes")
        Sedes.resize(824, 479)
        Sedes.setMinimumSize(QtCore.QSize(824, 479))
        Sedes.setMaximumSize(QtCore.QSize(824, 479))
        Sedes.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tx_buscar = QtWidgets.QLineEdit(Sedes)
        self.tx_buscar.setGeometry(QtCore.QRect(10, 10, 221, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.tx_buscar.setFont(font)
        self.tx_buscar.setObjectName("tx_buscar")
        self.radioButton_sede = QtWidgets.QRadioButton(Sedes)
        self.radioButton_sede.setGeometry(QtCore.QRect(340, 10, 82, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.radioButton_sede.setFont(font)
        self.radioButton_sede.setFocusPolicy(QtCore.Qt.TabFocus)
        self.radioButton_sede.setObjectName("radioButton_sede")
        self.bt_eliminar = QtWidgets.QPushButton(Sedes)
        self.bt_eliminar.setGeometry(QtCore.QRect(650, 420, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_eliminar.setFont(font)
        self.bt_eliminar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_eliminar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.bt_eliminar.setAutoDefault(False)
        self.bt_eliminar.setDefault(False)
        self.bt_eliminar.setFlat(False)
        self.bt_eliminar.setObjectName("bt_eliminar")
        self.tableWidgetSedes = QtWidgets.QTableWidget(Sedes)
        self.tableWidgetSedes.setGeometry(QtCore.QRect(10, 50, 801, 351))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidgetSedes.setFont(font)
        self.tableWidgetSedes.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tableWidgetSedes.setStyleSheet("QHeaderView::section {\n"
"    background-color:  rgb(7, 70, 124);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 12pt \"Verdana\";\n"
"    border: 0px solid #ff0000;\n"
"    height: 32px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    font: 11pt \"Verdana\";\n"
"    border: 1px solid;\n"
"}\n"
"\n"
"QTableWidget::item{\n"
"    selection-background-color: rgb(7, 70, 124);\n"
"    selection-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.tableWidgetSedes.setAutoScroll(True)
        self.tableWidgetSedes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetSedes.setTabKeyNavigation(False)
        self.tableWidgetSedes.setProperty("showDropIndicator", True)
        self.tableWidgetSedes.setDragEnabled(False)
        self.tableWidgetSedes.setDragDropOverwriteMode(True)
        self.tableWidgetSedes.setAlternatingRowColors(True)
        self.tableWidgetSedes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidgetSedes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetSedes.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidgetSedes.setShowGrid(True)
        self.tableWidgetSedes.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidgetSedes.setWordWrap(True)
        self.tableWidgetSedes.setCornerButtonEnabled(True)
        self.tableWidgetSedes.setRowCount(10)
        self.tableWidgetSedes.setColumnCount(2)
        self.tableWidgetSedes.setObjectName("tableWidgetSedes")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSedes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetSedes.setHorizontalHeaderItem(1, item)
        self.tableWidgetSedes.horizontalHeader().setVisible(True)
        self.tableWidgetSedes.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetSedes.horizontalHeader().setHighlightSections(False)
        self.tableWidgetSedes.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidgetSedes.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetSedes.verticalHeader().setVisible(False)
        self.tableWidgetSedes.verticalHeader().setHighlightSections(True)
        self.bt_modificar = QtWidgets.QPushButton(Sedes)
        self.bt_modificar.setGeometry(QtCore.QRect(330, 420, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_modificar.setFont(font)
        self.bt_modificar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_modificar.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.bt_modificar.setAutoDefault(False)
        self.bt_modificar.setDefault(False)
        self.bt_modificar.setFlat(False)
        self.bt_modificar.setObjectName("bt_modificar")
        self.radioButton_codigo = QtWidgets.QRadioButton(Sedes)
        self.radioButton_codigo.setGeometry(QtCore.QRect(250, 10, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.radioButton_codigo.setFont(font)
        self.radioButton_codigo.setFocusPolicy(QtCore.Qt.TabFocus)
        self.radioButton_codigo.setChecked(True)
        self.radioButton_codigo.setObjectName("radioButton_codigo")
        self.bt_nuevo = QtWidgets.QPushButton(Sedes)
        self.bt_nuevo.setGeometry(QtCore.QRect(10, 420, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_nuevo.setFont(font)
        self.bt_nuevo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bt_nuevo.setStyleSheet("background-color: rgb(7, 70, 124);\n"
"font: 18pt \"Verdana\";\n"
"border-radius: 10px;\n"
"color: rgb(255, 255, 255);")
        self.bt_nuevo.setAutoDefault(False)
        self.bt_nuevo.setDefault(False)
        self.bt_nuevo.setFlat(False)
        self.bt_nuevo.setObjectName("bt_nuevo")

        self.retranslateUi(Sedes)
        QtCore.QMetaObject.connectSlotsByName(Sedes)

        from Forms.Sede.ControllerSedes import ControllerSedes
        controller = ControllerSedes(self, Sedes, selectRegister, ref_tx_id_sede)

    def retranslateUi(self, Sedes):
        _translate = QtCore.QCoreApplication.translate
        Sedes.setWindowTitle(_translate("Sedes", "Sedes"))
        self.radioButton_sede.setText(_translate("Sedes", "Sede"))
        self.bt_eliminar.setText(_translate("Sedes", "Eliminar"))
        item = self.tableWidgetSedes.horizontalHeaderItem(0)
        item.setText(_translate("Sedes", "Código"))
        item = self.tableWidgetSedes.horizontalHeaderItem(1)
        item.setText(_translate("Sedes", "Sede"))
        self.bt_modificar.setText(_translate("Sedes", "Modificar"))
        self.radioButton_codigo.setText(_translate("Sedes", "Código"))
        self.bt_nuevo.setText(_translate("Sedes", "Nuevo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Sedes = QtWidgets.QDialog()
    ui = Ui_Sedes()
    ui.setupUi(Sedes)
    Sedes.show()
    sys.exit(app.exec_())
