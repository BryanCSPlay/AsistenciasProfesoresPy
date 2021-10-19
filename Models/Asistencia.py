class ModelAsistencia(object):
    def __init__(self):
        self.id_asistencia = 0
        self.dni_profesor = 0
        self.fecha = ""
        self.hora_entrada = ""
        self.hora_salida = ""
        self.estado = ""
        self.id_sede = ""
        self.id_ciclo = ""
        self.tardanza = ""
        self.restante = ""
        self.observacion = ""
        self.id_clase = 0

    def AsistenciaToList(self):
        rows = [(self.dni_profesor,
                 self.hora_entrada, self.hora_salida, self.tardanza, self.restante,
                 self.fecha, self.estado, self.id_sede, self.id_ciclo, self.observacion, self.id_clase)]

        return rows
