""" Clase para los barcos petroleros """

class Petrolero:
    """Barcos petroleros"""

    def __init__(self, tiempo):
        # instante de tiempo para la siguiente accion
        self.tiempo = tiempo
        # estado en el que se encuentra el barco petrolero
        self.estado = 0 # estado inicial
