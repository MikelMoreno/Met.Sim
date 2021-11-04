""" Programa main """

# Importar classes
from petrolero import Petrolero
from remolcador import Remolcador
# Importar funciones auxiliares
import utils
# Importar librerias linked list
from collections import deque


ESTADOS = {0, 1, 2, 3, 4, 5, 6} # Posibles estados
NUM_REMOLCADORES = 20 # Numero maximo de remolcadores

# Lista de remolcadores
remolcadores = [Remolcador() for i in range(NUM_REMOLCADORES)]

tiempos_llegada = utils.init_tiempos_petroleros()

array_petroleros = [Petrolero(t) for t in tiempos_llegada]

events_list = deque(array_petroleros)

