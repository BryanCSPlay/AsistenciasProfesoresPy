class ModelCiclo(object):
    def __init__(self):
        self.id_ciclo = 0
        self.ciclo = ""

    def CicloToList(self):
        rows = [(self.id_ciclo, self.ciclo)]
        return rows