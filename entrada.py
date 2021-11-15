#clase entrada

import queue

class Entrada:

    def _init_(self):
        self.cola_entrada = queue.Queue()

    def addBarco(self, barco):
        self.cola_entrada.put(barco)

    def getBarco(self):
        return self.cola_entrada.get()