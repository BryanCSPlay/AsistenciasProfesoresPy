class ModelClase(object):
    def __init__(self):
        self.id_division = 0
        self.dni_profesor = 0
        self.hora_entrada = ""
        self.hora_salida = ""
        self.dia = ""

    def ClaseToList(self):
        rows = [(self.id_division, self.dni_profesor,
                 self.hora_entrada, self.hora_salida, self.dia)]
        return rows
