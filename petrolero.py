""" Clase para los barcos petroleros """
#create a static variable
class Petrolero:
    """Barcos petroleros"""
    #create a static variable   
    __numero_petroleros = 0
    def __init__(self, tiempo):
        # instante de tiempo para la siguiente accion
        self.tiempo = tiempo
        # estado en el que se encuentra el barco petrolero
        self.estado = 0 # estado inicial
        #identifier
        self.id = ++Petrolero.__numero_petroleros