#clase estados
""" Archivo con las fases por las que pasa un petrolero """
class Estados:
    PETROLERO_LLEGA = 0
    PETROLERO_ESPERA_ENTRADA = 1
    PERTROLERO_CAMINO_A_MUELLE = 2
    PETROLERO_DESCARGA = 3
    PETROLERO_ESPERA_SALIDA = 4
    PETROLERO_FIN = 5
    #QUESTION: ¿es necesario introducir los estados del remolcador?