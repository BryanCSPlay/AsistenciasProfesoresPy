class ModelProfesor(object):
    def __init__(self):
        self.dni_profesor = 0
        self.apellido = ""
        self.nombre = ""
        self.fn = ""
        self.qr = ""

    def ProfesorToList(self):
        rows = [(self.dni_profesor, self.apellido, self.nombre, self.fn, self.qr)]
        return rows