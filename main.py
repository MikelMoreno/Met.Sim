""" Programa main """
import random
from estados import Estados as sts

#class main
class Main: 
    listaPetroleros=[]
    listaRemolcadores =[]
    muelles = 0
    tiempo_max = 50
    
    #init
    def __init__(self,remolcadores,muelles):
        # Lista de remolcadores
        self.listaPetroleros=ListPetroleros()
        self.listaRemolcadores = ListRemolcadores(remolcadores)
        self.muelles = muelles
        
        
    def between(self,value, min, max):
        if min <= value < max:
            return True
        else:
            return False
        
    def getPoissonRate(self,time):
        """ Método que devuelve el valor de la distribución de Poisson para un tiempo dado """
        lambd = 0
        h_in_day = (time / 60.0) % 24.0
        if self.between(h_in_day, 0.0, 5):
            lambd = 2.0 / 5.0 * h_in_day + 5.0
        elif self.between(h_in_day, 5, 8):
            lambd = -1.0 / 3.0 * h_in_day + 26.0 / 3.0
        elif self.between(h_in_day, 8, 15):
            lambd = 3.0 / 7.0 * h_in_day + 18.0 / 7.0
        elif self.between(h_in_day, 15, 17):
            lambd = -3.0 / 2.0 * h_in_day + 63.0/2.0
        elif self.between(h_in_day, 17, 24):
            lambd = -1.0 / 7.0 * h_in_day + 59.0 / 7.0
        else:
            print("Lambda fuera del rango")
            #logging.error("lambda out of index")
        return lambd

    # metodo que inicializa la llegada de todos los petroleros
    def init_tiempos_petroleros(self):
        """ Método que devuelve un array con 
        todos los tiempos de llegada de los petroleros """
        tiempo = 0
        # Calculamos el primero en llegar
        tiempo += 60 * random.expovariate(self.getPoissonRate(tiempo))
        self.listaPetroleros.añadirBarco(tiempo)
        # Mientras las llegadas esten dentro del tiempo de simulacion calculamos las siguientes entradas
        while tiempo < self.tiempo_max:
            tiempo += 60 * random.expovariate(self.getPoissonRate(tiempo))
            self.listaPetroleros.añadirBarco(tiempo)
    
    # funcion simular
    def simular(self):
        self.init_tiempos_petroleros()
        while self.listaPetroleros().final==False:
            petrolero = self.listaPetroleros[0]
            estadoPetrolero = petrolero[2]
            if estadoPetrolero == sts.PETROLERO_LLEGA:
                self.estado0(petrolero)
            elif estadoPetrolero == sts.PETROLERO_ESPERA_ENTRADA:
                self.estado1(petrolero)
            elif estadoPetrolero == sts.PERTROLERO_CAMINO_A_MUELLE:
                self.estado2(petrolero) # no existe
            elif estadoPetrolero == sts.PETROLERO_DESCARGA:
                self.estado3(petrolero) #no existe
            elif estadoPetrolero == sts.PETROLERO_ESPERA_SALIDA:
                self.estado4(petrolero)

    def estado0(self,petrolero):
        if self.listaRemolcadores.cola1()==False:
            remolcador = self.listaRemolcadores[0]
            tiempo = remolcador[1]
            if remolcador[2]==3:
                tiempo = ALEATORIO
                self.listaRemolcadores.modificar(tiempo,4,-1)
            self.listaPetroleros.modificar(tiempo,1,-1)
        else:
            tiempo =petrolero[1] + ALEATORIO
            remolcador = self.listaRemolcadores.getOneCola1()
            self.listaPetroleros.modificar(tiempo,2,remolcador[0])
            self.listaRemolcadores.modificar(tiempo,2,petrolero[0])

    def estado1(self,petrolero):
        if self.listaRemolcadores.cola1()==False:
            remolcador = self.listaRemolcadores[0]
            tiempo = remolcador[1]
            if remolcador[2]==3:
                tiempo = ALEATORIO
                self.listaRemolcadores.modificar(tiempo,4,-1)
            self.listaPetroleros.modificar(tiempo,1,-1)
        else:
            tiempo = ALEATORIO
            remolcador = self.listaRemolcadores.getOneCola1()
            self.listaPetroleros.modificar(tiempo,2,remolcador[0])
            self.listaRemolcadores.modificar(tiempo,2,petrolero[0])

    def estado4(self,petrolero):
        # si no hay remolcadores en cola2
        if self.listaRemolcadores.cola2()==False:
            tiempo = tiempo+ ESPERA
            #estado de espera para salir de la cola = 4
            #carguero no asignado = -1
            self.listaPetroleros.modificarBarco(self,tiempo,4, -1)
        else:
            #si hay remolcadores en cola2 SE VA AL ESTADO 5
            tiempo = tiempo + ALEATORIO_salida_del_puerto
            remolcador = self.listaRemolcadores.getOneCola2()
            self.listaPetroleros.modificarBarco(tiempo,5, remolcador[0])
            self.listaRemolcadores.modificarRemolcador(tiempo,4,petrolero[0])
            
            #IRSE SOLO si no hay remolcadores en la cola 2 y hay un barco que quiere salir
            if self.listaRemolcadores.cola2()==False and self.listaPetroleros.cola2()==True:
                tiempo = tiempo + ALEATORIO_regresa_muelle
                self.listaRemolcadores.modificarRemolcador(tiempo,4,petrolero[0])
            #QUEDARSE ESPERANDO
            else:
                self.listaRemolcadores.modificarRemolcador(tiempo,1,petrolero[0])
