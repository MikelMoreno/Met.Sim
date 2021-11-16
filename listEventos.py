class ListEventos():
    list = []

    def __init__(self):
        self.list=[]

    def añadirEvento(self, estado, tiempo, id = None):
        evento = [estado, tiempo, id]
        self.list.append(evento)
        self.list = sorted(self.list, key = lambda item: item[1])

    def numEventos(self):
        return len(self.list)

    def getEvento(self):
        return self.list.pop(0)
        