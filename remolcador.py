""" Clase para los remolcadores """

import random

class Remolcador:
    """Barcos remolcadores"""
    __numero_remolcadores = 0

    def __init__(self):
        # instante de tiempo para la siguiente accion
        self.tiempo = 0
        # estado en el que se encuentra el remolcador
        self.estado = 0 # estado inicial
        # boolean si el remolcador esta libre o ocupado
        self.libre = True
        #identificador del remolcador
        Remolcador.__numero_remolcadores += 1
        self.id = Remolcador.__numero_remolcadores

    def movimiento_puerto_muelle(self, mu, sigma, tiempo):
        """Calcula el tiempo que tarda el carguero en moverse y devuelve el tiempo 
        de finalizacion de la tarea"""
        return tiempo + random.normalvariate(mu, sigma)

