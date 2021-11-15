""" Clase para los barcos petroleros """
import numpy as np
from estados import Estados as sts
from evento import Evento

class Petrolero:
    """Barcos petroleros"""
    #create a static variable   
    __numero_petroleros = 0

    
    def __init__(self, tiempo):
        # instante de tiempo para la siguiente accion
        self.tiempo = tiempo
        self.estado = [None, None, None, None, None, None]
        #identifier
        Petrolero.__numero_petroleros += 1
        self.id = Petrolero.__numero_petroleros

        #listado de eventos por el que pasa el carguero inicializamos la llegada
        self.eventos = {self.estado: Evento(self.tiempo, self.estado)}
    
    def descarga(self, x, tiempo):
        """Calcula el tiempo que tarda el petrolero en descargar y devuelve el tiempo 
        de finalizacion de la tarea"""
        return tiempo + (60 * np.random.chisquare(x))

    def setEstado(self, estado, tiempo):
        self.estado[estado] = tiempo
        if (self.tiempo < tiempo):
            self.tiempo = tiempo
    
    def getEstado(self, estado):
        return self.estado[estado]

    def getId(self):
        return self.id
        

