from Class.Crud import ClassCrud
from Models.Clase import ModelClase

class ControllerAdvertenciaAsistencia(object):
    def __init__(self, Dialog, QDialog, id_clase, restante):
        self.Dialog = Dialog
        self.QDialog = QDialog

        self.load()

    def load(self):
        query = "SELECT * FROM tb_clases WHERE id_clase =" + self.id_clase
        currentClass = ClassCrud().GetWithIds(query)


