from estados import Estados as sts

##Clase Lista de Remolcadores
class ListaCargueros:
    
    def __init__(self,num):
        self.list=[]
        for i in range(num):
            carguero=[i,0,0,-1]
            self.list.append( carguero)
            
    def getById(self,id):
        res = []
        for barco in self.list:
            if barco[0]==id:
                res = barco
                break
        return res
            
    def modificar(self,iD,time,estado,petrolero):    
        carguero = self.getById(iD)
        num = self.getPosId(iD)
        carguero[1] = time
        carguero[2] = estado
        carguero[3] = petrolero
        self.list[num]=carguero
        self.list = sorted(self.list, key=self.comparator)
        
        
    def libreEntrada(self):
        res=False
        for carguero in self.list:
            if carguero[2]==0:
                res=True
                break
        return res
    
    def libreSalida(self):
        res=False
        for carguero in self.list:
            if carguero[2]==2:
                res=True
                break
        return res
    
    def getLibreEntrada(self):
        res = []
        for carguero in self.list:
            if carguero[2]==0:
                res = carguero
                break
        return res
    
    def getLibreSalida(self):
        res = []
        for carguero in self.list:
            if carguero[2]==2:
                res = carguero
                break
        return res