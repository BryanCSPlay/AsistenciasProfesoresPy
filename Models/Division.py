class ModelDivision(object):
    def __init__(self):
        self.id_division = 0
        self.division = ""
        self.id_materia = 0

    def DivisionToList(self):
        rows = [(self.id_division, self.division, self.id_materia)]
        return rows