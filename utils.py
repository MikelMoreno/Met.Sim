""" Archivo para funciones auxiliares """

import random
from constantes import *

#metodo que devuelde true si un valor esta entre dos valores
def between(value, min, max):
    if min <= value < max:
        return True
    else:
        return False

def getPoissonRate(time):
    """ Método que devuelve el valor de la distribución
        de Poisson para un tiempo dado """
    lambd = 0
    h_in_day = (time / 60.0) % 24.0
    if between(h_in_day, 0.0, 5):
        lambd = 2.0 / 5.0 * h_in_day + 5.0
    elif between(h_in_day, 5, 8):
        lambd = -1.0 / 3.0 * h_in_day + 26.0 / 3.0
    elif between(h_in_day, 8, 15):
        lambd = 3.0 / 7.0 * h_in_day + 18.0 / 7.0
    elif between(h_in_day, 15, 17):
        lambd = -3.0 / 2.0 * h_in_day + 63.0/2.0
    elif between(h_in_day, 17, 24):
        lambd = -1.0 / 7.0 * h_in_day + 59.0 / 7.0
    else:
        print("Lambda fuera del rango")
        #logging.error("lambda out of index")
    return lambd

def get_tiempo_vacio(tiempo):
    """ Método que devuelve el tiempo de movimiento
        para un remolcador vacío """
    return 60 * random.expovariate(tiempo + random.normalvariate(MU_REMOLCADOR_VACIO, SIGMA_REMOLCADOR_VACIO))

def get_tiempo_lleno(tiempo):
    """ Método que devuelve el tiempo de movimiento
        para un remolcador lleno """
    return 60 * random.expovariate(tiempo + random.normalvariate(MU_REMOLCADOR_LLENO, SIGMA_REMOLCADOR_LLENO))