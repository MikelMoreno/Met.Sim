from estados import Estados as sts
from petrolero import Petrolero

##Clase Lista de Barcos
class ListPetroleros():
    list = []
    
    def __init__(self):
        self.list=[]
        self.ultimoInsertado = None
        
    def comparator(self, barco):
        return barco[1]
        
    def añadirBarco(self, time):
        id = len(self.list) + 1
        barco = [id, time, sts.LLEGADA_A_PUERTO, 0]
        self.list.append(barco)
        self.list = sorted(self.list, key=self.comparator)

        self.ultimoInsertado = barco
        
    def cola1(self):
        res=False
        for barco in self.list:
            if barco[2] == sts.PETROLERO_ESPERA_ENTRADA:
                res=True
                break
        return res
    
    def cola2(self):
        res=False
        for barco in self.list:
            if barco[2] == sts.PETROLERO_ESPERA_SALIDA:
                res=True
                break
        return res
    
    def modificar(self,iD,time,estado,carguero):    
        petrolero = self.getById(iD)
        num = self.getPosId(iD)
        petrolero[1] = time
        petrolero[2] = estado
        petrolero[3] = carguero
        self.list[num]=petrolero
        self.list = sorted(self.list, key=self.comparator)

    def getPosId(self,iD):
        res=0
        for petrolero in self.list:
            if petrolero[0] == iD:
                break
            res = res+1
                
        return res     
    def getById(self,id):
        res = []
        for barco in self.list:
            if barco[0]==id:
                res = barco
                break
        return res
    
    def final(self):
        res = True
        for barco in self.list:
            if barco[2] != sts.PETROLERO_FIN:
                res = False
                break
        return res

    def comparator2(self, barco):
        return barco[0]

    def getLastInserted(self):
        return self.ultimoInsertado
            