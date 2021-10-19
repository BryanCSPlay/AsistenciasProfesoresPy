from PyQt5 import QtCore, QtGui, QtWidgets


class ClassColors(object):
    def __init__(self, Dialog):
        self.Dialog = Dialog

        for i in range(self.Dialog.tableWidget_hoy.rowCount()):
            index = self.Dialog.tableWidget_hoy.model().index(i, 13)
            indexState = self.Dialog.tableWidget_hoy.model().index(i, 11)

            if(str(self.Dialog.tableWidget_hoy.model().data(index)) != "None" and str(self.Dialog.tableWidget_hoy.model().data(indexState)) != "Ausencia"):
                if(int(self.Dialog.tableWidget_hoy.model().data(index)) > 0):
                    if(str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "Dentro del instituto" or str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "Fuera del instituto"):
                        for j in range(self.Dialog.tableWidget_hoy.columnCount()):
                            self.Dialog.tableWidget_hoy.item(i, j).setBackground(
                                QtGui.QBrush(QtGui.QColorConstants.Green))

                    elif(str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "Recuperación" or str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "Recuperación"):
                        for j in range(self.Dialog.tableWidget_hoy.columnCount()):
                            self.Dialog.tableWidget_hoy.item(i, j).setBackground(
                                QtGui.QBrush(QtGui.QColorConstants.Yellow))

            elif(str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "Ausencia"):
                for j in range(self.Dialog.tableWidget_hoy.columnCount()):
                    self.Dialog.tableWidget_hoy.item(i, j).setBackground(
                        QtGui.QBrush(QtGui.QColorConstants.Red))
                    self.Dialog.tableWidget_hoy.item(i, j).setForeground(
                        QtGui.QBrush(QtGui.QColorConstants.White))

            elif(str(self.Dialog.tableWidget_hoy.model().data(indexState)) == "None"):
                #print(str(self.Dialog.tableWidget_hoy.model().data(indexState)))
                item = QtWidgets.QTableWidgetItem(str("")) 
                self.Dialog.tableWidget_hoy.setItem(i, 11, item)  


# id_asistencia > 0 (Presente)
# id_asistencia == 0 (Ausente)
# id_asistencia == None (No marcado)
# tardanza == No aplica (Recuperacion)