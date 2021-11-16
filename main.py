""" Programa main """
# Importar classes
from petrolero import Petrolero
from remolcador import Remolcador
from muelle import Muelle
from entrada import Entrada
from listEventos import ListEventos
from listPetroleros import ListPetroleros
from listaCargueros import ListaCargueros
from estados import Estados as sts
# Importar funciones auxiliares
from utils import *
# Importar librerias linked list
from collections import deque
#importar constantes
from constantes import *

import random

#class main
class Main: 
    
    #init
    def __init__(
        self,
        num_remolcadores = NUM_REMOLCADORES,
        tiempo_max = TIEMPO_MAX,
        num_muelles = NUM_MUELLES,
        mu_remolcador_vacio = MU_REMOLCADOR_VACIO,
        sigma_remolcador_vacio = SIGMA_REMOLCADOR_VACIO,
        grado_libertad_descarga = GRADO_LIBERTAD_DESCARGA,
        sigma_remolcador_lleno = SIGMA_REMOLCADOR_LLENO,
        mu_remolcador_lleno = MU_REMOLCADOR_LLENO
    ):       
        self.muelles = num_muelles
        self.tiempo_max = tiempo_max
        self.mu_remolcador_vacio = mu_remolcador_vacio
        self.mu_remolcador_lleno = mu_remolcador_lleno
        self.sigma_remolcador_vacio = sigma_remolcador_vacio
        self.sigma_remolcador_lleno = sigma_remolcador_lleno
        self.grado_libertad_descarga = grado_libertad_descarga
        self.tiempo = 0

        # Lista de remolcadores
        self.listaCargueros = ListaCargueros(num_remolcadores)
        self.listaPetroleros= ListPetroleros()

        # definir el sistema
        # cola entrada
        self.colaEntrada = Entrada()
        # muelle (puestos_muelle y cola de salida)
        self.listaMuelles = Muelle(num_muelles)
        self.listaEventos = ListEventos()
    
    # funcion simular
    def simular(self):
        cont = 0
        # Calculamos el primero en llegar
        tiempo = 60 * random.expovariate(getPoissonRate(self.tiempo))
        
        if tiempo > self.tiempo_max:
            print("No han llegado cargueros durante la simulación")
            return -1
        

        self.listaEventos.añadirEvento(sts.LLEGADA_A_PUERTO, tiempo)
        while self.listaEventos.numEventos() > 0:
            #POP
            evento = self.listaEventos.getEvento()
            id = evento[2] # id del petrolero o del carguero (segun el vento recogido)
            id_evento = evento[0] # id del evento recogido
            tiempo = evento[1]
            self.tiempo = tiempo


            if(id_evento == sts.LLEGADA_A_PUERTO):
                self.eventoLLegada()
            elif(id_evento == sts.CARGUERO_ENTRADA_MUELLE_LLENO):
                self.eventoPuertoMuelleLleno(id)
            elif(id_evento == sts.CARGUERO_ENTRADA_MUELLE_VACIO):
                self.eventoPuertoMuelleVacio(id)
            elif(id_evento == sts.CARGUERO_MUELLE_ENTRADA_LLENO):
                self.eventoMuellePuertoLleno(id)
            elif(id_evento == sts.CARGUERO_MUELLE_ENTRADA_VACIO):
                self.eventoMuellePuertoVacio(id)
            elif(id_evento == sts.PETROLERO_DESCARGA):
                self.eventoDescarga(id)
            else:
                print("Error: Evento desconocido")



    #Calculo si lanzo eventoPuertoMuelleLleno o meto en la cola. Calculo siguiente llegada.¿Calculamos posible eventoMuellePuertoVacio?  
    def eventoLLegada(self):
        self.listaPetroleros.añadirBarco(self.tiempo)
        iD = self.listaPetroleros.getLastInserted()

        #Calculo siguiente entrada
        tiempoSiguiente = self.tiempo + 60 * random.expovariate(getPoissonRate(self.tiempo))
        if tiempoSiguiente <= self.tiempo_max:
            self.listaEventos.añadirEvento(sts.LLEGADA_A_PUERTO,tiempoSiguiente,iD)
        #Si no hay cola y hay muelles libres
        if self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            #Ademas hay cargueros disponibles hago CARGUERO_ENTRADA_MUELLE_LLENO
            if self.listaCargueros.libreEntrada():
                #tiempo de llegada a muelle por remolcador lleno siguiendo una distribución normal
                tiempo = self.tiempo + 60 * random.expovariate(self.tiempo + random.normalvariate(self.mu_remolcador_lleno, self.sigma_remolcador_lleno))
                carguero = self.listaCargueros.getLibreEntrada()
                self.listaCargueros.modificar(carguero[0],tiempo,1,iD)
                self.listaPetroleros.modificar(iD,tiempo,1,carguero[0])
               
                petrolero = self.listaPetroleros.getById(iD)
                self.listaMuelles.addBarcoMuelle(petrolero)
                
                self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempo,carguero[0])
                #Si no hay cargueros disponibles en la entrada pero si en salida hago CARGUERO_MUELLE_ENTRADA_VACIO
            elif self.listaCargueros.libreSalida:
                tiempo = self.tiempo + 60 * random.expovariate(self.tiempo + random.normalvariate(self.mu_remolcador_vacio, self.sigma_remolcador_vacio))
                carguero = self.listaCarguero.getLibreSalida()
                 #TENDRIA QUE ASIGNARLE YA EL CARGUERO?

                #Y AL CONTRARIO¿
                self.listaCargueros.modificar(carguero[0],tiempo,3,iD)
                
                
                petrolero = self.listaPetroleros.getById(iD)
                self.colaEntrada.addBarco(petrolero)
                
                self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_VACIO,tiempo,carguero[0])
  
        else:
            petrolero = self.listaPetroleros.getById(iD)
            self.colaEntrada.addBarco(petrolero)
            

    
    
    #Calculo si lanzo eventoMuellePuertoLleno o eventoMuellePuertoVacio y eventoDescarga.
    def eventoPuertoMuelleLleno(self, iD):
        #El evento descarga siempre se hace
        tiempoDescarga = t + (60 * np.random.chisquare(self.tiempo))
        carguero = self.listaCarguero.getById(iD)
        self.listaPetroleros.modificar(carguero[3],tiempoDescarga,4,-1)
        self.listaCarguero.modificar(iD,tiempoDescarga,2,-1)

        self.listaEventos.añadirEvento(sts.PETROLERO_DESCARGA,tiempoDescarga,petrolero[0])
        #Si no hay colaSalida, si hay colaEntrada y hay muelles disponibles
        #VUELVO VACIO
        if self.colaSalida.isEmpty() and !self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoSolo = t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,3,-1)
            self.listaEventos.añadirEvento(4,tiempoSolo,iD)
        #Si hay cola de salida
        #VUELVO LLENO
        if !self.colaSalida.isEmpty():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaSalida.popBarcoEspera()
            self.listaCargueros.modificar(iD,tiempoLleno,3,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,3,iD)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,iD)
        
    
    #Calculo si lanzo eventoMuellePuertoLleno o ¿eventoMuellePuertoVacio?
    def eventoPuertoMuelleVacio(self, iD):
        self.listaCarguero.modificarPorId(iD,self.t,2,-1)
        #Vuelvo vacio
        #Si no hay cola salida y si la cola entrada.
        if self.colaSalida.isEmpty() and !self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoSolo= t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,3,-1)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_VACIO,tiempoSolo,iD)
        #Vuelvo lleno
        #Si hay cola 
        elif !self.colaSalida.isEmpty():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaSalida.popBarcoEspera()
            self.listaCarguero.modificar(iD,tiempoLleno,3,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,3,iD)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,iD)

    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoLleno(self, iD):
        carguero = self.listaCarguero.getById(iD)
        self.listaCargueros.modificar(iD,self.t,0,-1)
        self.listaPetroleros.modificar(carguero[3],carguero[1],6,-1)
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaEntrada.isEmpty() and !self.colaSalida.isEmpty:
            tiempoSolo= t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,1,-1)

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoSolo,iD)
        #Vuelvo lleno
        #Si hay cola y muelles
        elif self.colaEntrada.Lleno() and self.listaMuelles.libre():
            tiempoLleno = t+ get_tiempo_lleno(tiempo)
            petrolero = self.colaEntrada.popBarcoEspera()
            self.listaCarguero.modificar(iD,tiempoLleno,1,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,1,iD)
            self.listaMuelles.addBarcoMuelle()

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempoLleno,iD)
    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoVacio(self, iD):
        carguero = self.listaCarguero.getById(iD)
        self.listaCargueros.modificar(iD,self.t,0,-1)
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaEntrada.isEmpty() and !self.colaSalida.isEmpty():
            tiempoSolo = t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,1,-1)

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoSolo,iD)
        #Vuelvo lleno
        #Si hay cola y muelles
        elif !self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaEntrada.popBarcoEspera()
            self.listaCarguero.modificar(iD,tiempoLleno,1,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,1,iD)
            self.listaMuelles.addBarcoMuelle()

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempoLleno,iD)
    
    #Calculo si lanzo eventoMuellePuertoLleno o meto en la cola o eventoPuertoMuelleVacio.
    def eventoDescarga(self, iD):
        
        self.listaPetroleros.modificar(iD,self.time,2,-1)
        petrolero = self.listaPetrolero.getById(iD)

        if self.listaCargueros.libreSalida:
            carguero = self.listaCargueros.getLibreSalida()
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            self.listaCargueros.modificar(carguero[0],tiempoLleno,3,iD)
            self.listaPetroleros.modificar(iD,tiempoLleno,3,carguero[0])
            self.listaMuelles.eliminar()

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,carguero[0])
            #ASIGNO YA EL CARGUERO?

        elif self.listaCargueros.libreEntrada:
            carguero = self.listaCargueros.getLibreEntrada()
            tiempoVacio= t + get_tiempo_vacio(tiempo)
            self.listaCargueros.modificar(carguero[0],tiempoVacio,1,-1)
            self.colaSalida.append(petrolero)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_VACIO,tiempoVacio,carguero[0])

        elif !self.colaSalida.isEmpty():
            self.colaSalida.addBarcoEspera(petrolero)

if __name__ == '__main__':
    simul = Main()
    simul.simular()

