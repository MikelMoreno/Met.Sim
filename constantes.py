ESTADOS = {0, 1, 2, 3, 4, 5, 6} # Posibles estados 
# TODO: mover estados a clase estados

NUM_REMOLCADORES = 10 # Numero maximo de remolcadores
NUM_MUELLES = 20 # Numero maximo de muelles
TIEMPO_MAX = 7*24*60 # Tiempo maximo de simulacion en minutos (7 dias)
SIGMA_REMOLCADOR_VACIO = 1 # Desviacion estandar de tiempo de REMOLCADOR_VACIO
MU_REMOLCADOR_VACIO = 2 # Media de tiempo de REMOLCADOR_VACIO
# SIGMA_REMOLCADOR_LLENO = sigma # Desviacion estandar de tiempo de REMOLCADOR_LLENO
# MU_REMOLCADOR_LLENO = mu # Media de tiempo de REMOLCADOR_LLENO
GRADO_LIBERTAD_DESCARGA = 2 # Grado de libertad de la distribucion de tiempo de DESCARGA