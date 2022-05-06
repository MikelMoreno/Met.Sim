from constantes import *
import numpy as np
import random


def estado_inicial():
    return random.randint(2,5) # estado inicial: un estado de desplazamiento


def estado_siguiente(estado):
    r = random.random()
    accum = 0
    for index, prob in enumerate(TABLA_ALIAS[estado]):
        accum = accum+prob
        if r < accum:
            return index

def getGravedadRandom():
    x = random.randint(0, 100) # para sacar un porcentaje
    fin = False
    prob = 0
    pos = 0
    while (not fin and pos < len(PROB_SERVICIOS)):
        prob += PROB_SERVICIOS[pos]
        if (x <= prob):
            fin = True
        else:
            pos += 1
    
    return pos


def simular(ejercicio):
    t = 0
    estado = estado_inicial()
    tiempo_desplazamientos = 0
    servicios_totales = 0
    
    tiempos_aranjuez_ocaña = []
    tiempo_accumulado_a_o = 0
    contador_tiempo = False


    while (t < T_MAX):

        if ejercicio == EJERCICIO_A or estado > 1:
            t_servicio = np.random.exponential(TIEMPO_ESTADO[estado])

        elif ejercicio == EJERCICIO_B:
            gravedad = getGravedadRandom()
            m_servicio = MEDIA_MINS_SERVICIO_CAT[gravedad]
            v_servicio = VARIANZA_SERVICIO_CAT[gravedad]
            t_servicio = random.normalvariate(m_servicio, v_servicio)

        if estado > 1: # estado es de desplazamiento
            tiempo_desplazamientos += t_servicio
        else: # estado es de servicio
            servicios_totales += 1

        t = t + t_servicio

        if contador_tiempo == True:
            tiempo_accumulado_a_o += t_servicio

        if estado == 1 and contador_tiempo == False:
            contador_tiempo = True

        if estado == 0 and contador_tiempo == True:
            tiempos_aranjuez_ocaña.append(tiempo_accumulado_a_o)
            tiempo_accumulado_a_o = 0
            contador_tiempo = False

        estado = estado_siguiente(estado)

    if VERBOSE == 1:
        print("Tiempo total de ejecución: ",t," minutos")
        print("Tiempo empleado en desplazamientos: ",tiempo_desplazamientos)
        print("Número medio de servicios al mes: ",servicios_totales)
        print("Tiempo medio aranjuez - ocaña: ",sum(tiempos_aranjuez_ocaña)/len(tiempos_aranjuez_ocaña))
    else:
        print(round(t,2),
                round(tiempo_desplazamientos,2),
                round(servicios_totales,2),
                round(sum(tiempos_aranjuez_ocaña)/len(tiempos_aranjuez_ocaña))
                )

simular("A")