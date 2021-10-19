class ModelMateria(object):
    def __init__(self):
        self.id_materia = 0
        self.materia = ""

    def MateriaToList(self):
        rows = [(self.id_materia, self.materia)]
        return rows