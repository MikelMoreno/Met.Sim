class ListEventos():
    list=[]

    def __init__(self):
        self.list=[]

    def añadirEvento(self,idPetrolero,tiempo,estado,idCarguero):
        evento = [idPetrolero,tiempo,estado,idCarguero]
        self.append(evento)