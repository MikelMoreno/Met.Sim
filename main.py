""" Programa main """
# Importar classes
from petrolero import Petrolero
from remolcador import Remolcador
from muelle import Muelle
from entrada import Entrada
from listEventos import ListEventos
from listPetroleros import ListPetroleros
from listRemolcadores import ListRemolcadores
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
        self.listaCargueros = ListRemolcadores(num_remolcadores)
        self.listaPetroleros= ListPetroleros()

        # definir el sistema
        # cola entrada
        self.colaEntrada = Entrada()
        # muelle (puestos_muelle y cola de salida)
        self.listaMuelles = Muelle()
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
                exit()



    #Calculo si lanzo eventoPuertoMuelleLleno o meto en la cola. Calculo siguiente llegada.¿Calculamos posible eventoMuellePuertoVacio?  
    def eventoLLegada(self):
        #Calculo siguiente entrada
        tiempoSiguiente = self.tiempo + 60 * random.expovariate(getPoissonRate(self.tiempo))
        if tiempoSiguiente <= self.tiempo_max:
            self.listaPetroleros.añadirBarco(tiempoSiguiente)
            self.listaEventos.añadirEvento(sts.LLEGADA_A_PUERTO,tiempoSiguiente)

        
        if self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            # Oier: he llegado hasta aqui tenemos que ver como organizar la lista de cargueros
            if self.listaCargueros.libreEntrada():
                #tiempo de llegada a muelle por remolcador lleno siguiendo una distribución normal
                tiempo = self.tiempo + 60 * random.expovariate(self.tiempo + random.normalvariate(self.mu_remolcador_lleno, self.sigma_remolcador_lleno))
                carguero = self.listaCarguero.getLibreEntrada()
                self.listaCargueros.modificar(carguero[0],tiempo,1,iD)
                self.listaPetroleros.modificar(iD,tiempo,1,carguero[0])
               
                
                petrolero = self.listaPetroleros.getById(iD)
                self.listaMuelles.append(petrolero)
                
                self.listaEventos.añadirEvento(1,tiempo)
                
                #TENDRIA QUE ASIGNARLE YA EL CARGUERO?
            elif self.listaCargueros.libreSalida:
                tiempo = self.tiempo + 60 * random.expovariate(self.tiempo + random.normalvariate(self.mu_remolcador_vacio, self.sigma_remolcador_vacio))
                carguero = self.listaCarguero.getLibreEntrada()
                
                #Y AL CONTRARIO¿
                self.listaCargueros.modificar(carguero[0],tiempo,1,iD)
                
                
                petrolero = self.listaPetroleros.getById(iD)
                self.colaEntrada.append(petrolero)
                
                self.listaEventos.añadirEvento(4,tiempo)

            
        else:
            petrolero = self.listaPetroleros.getById(iD)
            self.colaEntrada.append(petrolero)
            

    
    
    #Calculo si lanzo eventoMuellePuertoLleno o eventoMuellePuertoVacio y eventoDescarga.
    def eventoPuertoMuelleLleno(self, iD):
        tiempoDescarga = t + (60 * np.random.chisquare(self.tiempo))
        carguero = self.listaCarguero.getById(iD)
        self.listaPetroleros.modificar(carguero[3],tiempoDescarga,5,-1)
        self.listaCarguero.modificar(iD,tiempoDescarga,2,-1)
        self.listaEventos.añadirEvento(2,tiempoDescarga,iD)
        #Si no hay colaSalida, si hay colaEntrada y hay muelles disponibles
        #VUELVO VACIO
        if self.colaSalida.isEmpty() and self.colaEntrada.Lleno() and self.listaMuelles.libre():
            tiempoSolo = t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,3,-1)
            self.listaEventos.añadirEvento(4,tiempoSolo,iD)
        #Si hay cola de salida
        #VUELVO LLENO
        if self.colaSalida.Lleno():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaSalida[0]
            self.listaCargueros.modificar(iD,tiempoLleno,3,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,3,iD)
            self.listaMuelles.eliminar(iD)
            self.listaEventos.añadirEvento(3,tiempoLleno)
        
    
    #Calculo si lanzo eventoMuellePuertoLleno o ¿eventoMuellePuertoVacio?
    def eventoPuertoMuelleVacio(self, iD):
        self.listaCarguero.modificarPorId(iD,self.t,2,-1)
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaSalida.isEmpty() and self.colaEntrada.Lleno() and self.listaMuelles.libre():
            tiempoSolo= t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,1,-1)
            self.listaEventos.añadirEvento(2,tiempoSolo)
        #Vuelvo lleno
        #Si hay cola 
        elif self.colaSalida.Lleno():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaEntrada.lista[0]
            self.listaCarguero.modificar(iD,tiempoLleno,1,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,3,iD)
            self.listaEventos.añadirEvento(1,tiempoLleno)
    
    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoLleno(self, iD):
        carguero = self.listaCarguero.modificar
        self.listaPetroleros.modificar(iD,carguero[1],0,-1)
        self.listaPetroleros.modificar(carguero[3],carguero[1],6,-1)
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaEntrada.isEmpty() and self.colaSalida.Lleno():
            tiempoSolo= t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,1,-1)
            self.listaEventos.añadirEvento(2,tiempoSolo)
        #Vuelvo lleno
        #Si hay cola y muelles
        elif self.colaEntrada.Lleno() and self.listaMuelles.libre():
            tiempoLleno = t+ get_tiempo_lleno(tiempo)
            petrolero = self.colaEntrada.lista[0]
            self.listaCarguero.modificar(iD,tiempoLleno,1,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,1,iD)
            self.listaEventos.añadirEvento(1,tiempoLleno)
    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoVacio(self, iD):
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaEntrada.isEmpty() and self.colaSalida.Lleno():
            tiempoSolo = t + get_tiempo_vacio(tiempo)
            self.listaCarguero.modificar(iD,tiempoSolo,1,-1)
            self.listaEventos.añadirEvento(2,tiempoSolo)
        #Vuelvo lleno
        #Si hay cola y muelles
        elif self.colaEntrada.Lleno() and self.listaMuelles.libre():
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            petrolero = self.colaEntrada.lista[0]
            self.listaCarguero.modificar(iD,tiempoLleno,1,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,1,iD)
            self.listaEventos.añadirEvento(1,tiempoLleno)
    
    #Calculo si lanzo eventoMuellePuertoLleno o meto en la cola o eventoPuertoMuelleVacio.
    def eventoDescarga(self, iD):
        petrolero = self.listaPetrolero.getById(iD)
        if self.listaCargueros.libreSalida:
            carguero = self.listaCargueros.getLibreSalida()
            tiempoLleno = t + get_tiempo_lleno(tiempo)
            self.listaCargueros.modificar(carguero[0],tiempoLleno,3,iD)
            self.listaPetroleros.modificar(iD,tiempoLleno,3,carguero[0])
            self.listaMuelles.eliminar(iD)
            self.listaEventos.añadirEvento(3,tiempoLleno)
            #ASIGNO YA EL CARGUERO?
        elif self.listaCargueros.libreEntrada:
            carguero = self.listaCargueros.getLibreEntrada()
            tiempoVacio= t + get_tiempo_vacio(tiempo)
            self.listaCargueros.modificarPorId(carguero[0],tiempoVacio,1,-1)
            self.listaEventos.añadirEvento(2,tiempoVacio)
            self.colaSalida.append(petrolero)
        elif self.colaSalida.Lleno():
            self.colaSalida.append(petrolero)

if __name__ == '__main__':
    simul = Main()
    simul.simular()
            