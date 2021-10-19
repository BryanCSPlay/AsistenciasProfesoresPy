class ModelSede(object):
    def __init__(self):
        self.id_sede = 0
        self.sede = ""

    def SedeToList(self):
        rows = [(self.id_sede, self.sede)]
        return rows