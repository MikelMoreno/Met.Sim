""" Programa main """

# Importar classes
from petrolero import Petrolero
from remolcador import Remolcador
from estados import Estados
# Importar funciones auxiliares
import utils
# Importar librerias linked list
from collections import deque
#importar constantes
from constantes import *


#class main
class Main: 
    # Lista de remolcadores
    remolcadores = [Remolcador() for i in range(NUM_REMOLCADORES)]

    tiempos_llegada = utils.init_tiempos_petroleros()

    array_petroleros = [Petrolero(t) for t in tiempos_llegada]

    events_list = deque(array_petroleros)

    # funcion simular
    def simular(self):
        pass

    #init
    def __init__(self):
        pass


Main()