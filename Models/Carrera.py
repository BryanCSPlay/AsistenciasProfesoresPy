class ModelCarrera(object):
    def __init__(self):
        self.id_carrera = 0
        self.carrera = ""

    def CarreraToList(self):
        rows = [(self.id_carrera, self.carrera)]
        return rows