#clase estados
""" Archivo con las fases por las que pasa un petrolero """
class Estados:
    PETROLERO_LLEGA = 0
    PETROLERO_ESPERA_ENTRADA = 1
    PERTROLERO_CAMINO_A_MUELLE = 2
    PETROLERO_DESCARGA = 3
    PETROLERO_ESPERA_SALIDA = 4
    PETROLERO_FIN = 5

    CARGUERO_COLA_ENTRADA = 1
    CARGUERO_DIRECCION_MUELLE = 2
    CARGUERO_COLA_MUELLE = 3
    CARGUERO_DIRECCION_PUERTO = 4