#clase muelle
import queue

class Muelle:

    def __init__(self):
        self.barcos_en_muelle = 0
        self.cola_salida = queue.Queue()

    def addBarcoEspera(self, barco):
        self.cola_salida.put(barco)

    def addBarcoMuelle(self):
        self.barcos_en_muelle += 1