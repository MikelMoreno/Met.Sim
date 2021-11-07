##Clase Lista de Remolcadores
class ListRemolcadores():
    list = []
    
    def __init__(self,num):
        self.lista=[]
        for i in range(num):
            remolcador=[i,0,1,-1]
            self.list.append( remolcador)
        
    def comparator(self, remolcador):
        return remolcador[1]
        
    def cola1(self):
        res=False
        for remolcador in self.list:
            if remolcador[2]==1:
                res=True
                break
        return res

    def getOneCola1(self):
        res = []
        for remolcador in self.list:
            if remolcador[2]==1:
                res=remolcador
                break
        return res
    
    def cola2(self):
        res=False
        for remolcador in self.list:
            if remolcador[2]==3:
                res=True
                break
        return res

    def getOneCola2(self):
        res = []
        for remolcador in self.list:
            if remolcador[2]==3:
                res=remolcador
                break
        return res
    
    def modificarRemolcador(self,time,estado,barco):
        remolcador = self.list[0]
        remolcador[1] = remolcador[1]+time
        remolcador[2] = estado
        remolcador[3] = barco
        self.list[0]=remolcador
        self.list = sorted(self.list, key=self.comparator)
        
    def getById(self,id):
        res = []
        for remolcador in self.list:
            if remolcador[0]==id:
                res = remolcador
                break
        return res