from estados import Estados as sts

##Clase Lista de Barcos
class ListPetroleros():
    list = []
    
    def __init__(self):
        self.list=[]
        
    def comparator(self, barco):
        return barco[1]
        
    def añadirBarco(self,time):
        id = len(self.list)
        barco = [id, time, sts.PETROLERO_LLEGA, 0]
        self.list.append(barco)
        self.list = sorted(self.list, key=self.comparator)
        
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
    
    def modificarBarco(self,time,estado,carguero):
        barco = self.list[0]
        barco[1] = barco[1]+time #tiempo
        barco[2] = estado
        barco[3] = carguero #carguero asignado
        self.list[0]=barco
        self.list = sorted(self.list, key=self.comparator)
        
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
            