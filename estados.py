#clase estados
""" Archivo con las fases por las que pasa un petrolero """
class Estados:
    LLEGADA_A_PUERTO = 0
    CARGUERO_ENTRADA_MUELLE_LLENO = 1
    CARGUERO_ENTRADA_MUELLE_VACIO = 2
    CARGUERO_MUELLE_ENTRADA_LLENO = 3
    CARGUERO_MUELLE_ENTRADA_VACIO = 4
    PETROLERO_DESCARGA = 5

    CARGUERO_COLA_ENTRADA = 1
    CARGUERO_DIRECCION_MUELLE = 2
    CARGUERO_COLA_MUELLE = 3
    CARGUERO_DIRECCION_PUERTO = 4