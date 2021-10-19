class ModelMateriaCarrera(object):
    def __init__(self):
        self.id_materia = 0
        self.id_carrera = 0
        self.years = 0

    def MateriaCarreraToList(self):
        rows = [(self.id_materia, self.id_carrera, self.years)]
        return rows