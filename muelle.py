#clase muelle
import queue

class Muelle:

    def __init__(self, max_barcos):
        self.max_barcos = max_barcos
        self.barcos_en_muelle = 0
        self.cola_salida = queue.Queue()

    def addBarcoEspera(self, barco):
        self.cola_salida.put(barco)

    def popBarcoEspera(self):
        barco = self.cola_salida.pop()
        self.barcos_en_muelle -= 1
        return barco

    def addBarcoMuelle(self):
        self.barcos_en_muelle += 1

    def libre(self):
        return self.max_barcos != self.barcos_en_muelle