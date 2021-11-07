""" Programa main """

# Importar classes
from petrolero import Petrolero
from remolcador import Remolcador
from estados import Estados
# Importar funciones auxiliares
from utils import *
# Importar librerias linked list
from collections import deque
#importar constantes
from constantes import *

import random


#class main
class Main: 

    #init
    def __init__(
        self,
        num_remolcadores = NUM_REMOLCADORES,
        tiempo_max = TIEMPO_MAX,
        mu_remolcador_vacio = MU_REMOLCADOR_VACIO,
        sigma_remolcador_vacio = SIGMA_REMOLCADOR_VACIO,
        grado_libertad_descarga = GRADO_LIBERTAD_DESCARGA
    ):
        self.tiempo_max = tiempo_max
        self.mu_remolcador_vacio = mu_remolcador_vacio
        self.sigma_remolcador_vacio = sigma_remolcador_vacio
        self.grado_libertad_descarga = grado_libertad_descarga

        # Lista de remolcadores
        self.lista_remolcadores = [Remolcador() for i in range(num_remolcadores)]
        tiempos_llegada = self.init_tiempos_petroleros()
        self.array_petroleros = [Petrolero(t) for t in tiempos_llegada]

        self.events_list = deque(self.array_petroleros)

    # funcion simular
    def simular(self):
        # TODO
        pass
    
    # metodo que inicializa la llegada de todos los petroleros
    def init_tiempos_petroleros(self):
        """ Método que devuelve un array con 
        todos los tiempos de llegada de los petroleros """
        tiempo = 0
        tiempos_llegada = []

        # Calculamos el primero en llegar
        tiempo += 60 * random.expovariate(getPoissonRate(tiempo))
        # Mientras las llegadas esten dentro del tiempo de simulacion calculamos las siguientes entradas
        while tiempo < self.tiempo_max:
            tiempos_llegada.append(tiempo)
            tiempo += 60 * random.expovariate(getPoissonRate(tiempo))
        
        return tiempos_llegada


    

if __name__ == '__main__':
    simul = Main()
    simul.simular()