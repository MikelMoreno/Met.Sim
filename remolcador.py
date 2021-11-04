""" Clase para los remolcadores """

class Remolcador:
    """Barcos remolcadores"""
    static_count = 0
    def __init__(self):
        # instante de tiempo para la siguiente accion
        self.tiempo = 0
        # estado en el que se encuentra el remolcador
        self.estado = 0 # estado inicial
        # boolean si el remolcador esta libre o ocupado
        self.libre = True
        #identificador del remolcador
        self.id = ++Remolcador.static_count
