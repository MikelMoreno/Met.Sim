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
import numpy as np

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
        #estadisticos
        self.tiempoMedioAtracar = 0
        self.tiempoMaxAtracar = 0
        self.mediaBarcosMuelle = 0
        self.mediaEspera = 0
        self.mediaBarcosCola = 0
        self.maxBarcosCola = 0
        self.maxEspera = 0


        #actualización de estadisticos
    def actualizarEstadisticos(self,tAtraco,tCola, nCola):
        if tAtraco > self.tiempoMaxAtracar:
            self.tiempoMaxAtracar = tAtraco
        if tCola > self.maxEspera :
            self.maxEspera = tCola
        if nCola > self.maxBarcosCola:
            self.maxBarcosCola = nCola
        self.mediaBarcosCola += tCola
        self.tiempoMedioAtracar += tAtraco
        self.mediaEspera += tCola

    def actualizarBarcosMuelle(self,tMuelle):
        self.mediaBarcosMuelle += tMuelle

    def finalizarEstadisticos(self):
        self.tiempoMedioAtracar = self.tiempoMedioAtracar/len(self.listaPetroleros.list)
        self.mediaBarcosMuelle = self.mediaBarcosMuelle/self.tiempo
        self.mediaEspera = self.mediaEspera/len(self.listaPetroleros.list)
        self.mediaBarcosCola = self.mediaBarcosCola/self.tiempo
        print('Simulacion con ' + str(NUM_MUELLES) + ' muelles y' + str(NUM_REMOLCADORES) + ' cargueros')
        print("Tiempo medio en atracar: " + str(self.tiempoMedioAtracar))
        print("Tiempo maximo en atracar:" + str(self.tiempoMaxAtracar))
        print("Media de barcos en muelles:" + str(self.mediaBarcosMuelle))
        print("Media tiempo de espera en la entrada:" + str(self.mediaEspera))
        print("Maximo tiempo de espera en la entrada:" + str(self.maxEspera))
        print("Media de barcos esperando en la entrada:" + str(self.mediaBarcosCola))
        print("Maximo de barcos esperando en la entrada:" + str(self.maxBarcosCola))
        print("Tiempo total de simulacion:" + str(self.tiempo))

    # funcion simular
    def simular(self):
        cont = 0
        # Calculamos el primero en llegar
        tiempo = 60 * random.expovariate(getPoissonRate(self.tiempo))
        
        if tiempo > self.tiempo_max:
            print("No han llegado cargueros durante la simulación")
            return -1
        
        else:
            self.listaEventos.añadirEvento(sts.LLEGADA_A_PUERTO, tiempo)
            while self.listaEventos.numEventos() > 0:
                #print("EVENTOS")
                #print(self.listaEventos.list)
                #print("BARCOS")
                #print(self.listaPetroleros.list)
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
            self.finalizarEstadisticos()



    #Calculo si lanzo eventoPuertoMuelleLleno o meto en la cola. Calculo siguiente llegada.¿Calculamos posible eventoMuellePuertoVacio?  
    def eventoLLegada(self):
        self.listaPetroleros.añadirBarco(self.tiempo)
        petrolero = self.listaPetroleros.getLastInserted()
        iD = petrolero[0]
        #Calculo siguiente entrada
        tiempoSiguiente = self.tiempo + 60 * random.expovariate(getPoissonRate(self.tiempo))
        if tiempoSiguiente <= self.tiempo_max:
            self.listaEventos.añadirEvento(sts.LLEGADA_A_PUERTO,tiempoSiguiente)
        
        if not self.colaEntrada.isEmpty():
            self.colaEntrada.addBarco(petrolero)

        #Si no hay cola y hay muelles libres
        elif self.listaMuelles.libre():
            #Ademas hay cargueros disponibles hago CARGUERO_ENTRADA_MUELLE_LLENO
            if self.listaCargueros.libreEntrada():
                #tiempo de llegada a muelle por remolcador lleno siguiendo una distribución normal
                tiempo = self.tiempo + random.normalvariate(self.mu_remolcador_lleno, self.sigma_remolcador_lleno)
                carguero = self.listaCargueros.getLibreEntrada()
                self.listaCargueros.modificar(carguero[0],tiempo,sts.CARGUERO_DIRECCION_MUELLE,iD)

                # Oier: esto de aqui no tiene sentido, el petrolero no puede 
                # estar en evento 1 es un evento de carguero
                # esto se debe de actualizar cuando el carguero llega al muelle si 
                # lleva un barco porque entonces es cuando ha terminado el evento
                #
                # self.listaPetroleros.modificar(iD,tiempo,1,carguero[0])
               
                # actualizamos el muelle para reservarlo al barco
                self.listaMuelles.addBarcoMuelle() 
                self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempo,carguero[0])
                
                #Estadisticas
                petrolero = self.listaPetroleros.getById(iD)
                tiempoAtraco = tiempo - petrolero[1]
                tiempoEspera = self.tiempo - petrolero[1]
                self.actualizarEstadisticos(tiempoAtraco,tiempoEspera,0)
            
            else:
                self.colaEntrada.addBarco(petrolero)

                # si hay un carguero esperando en el muelle le decimos que venga a recoger
                if self.listaCargueros.libreSalida():
                    tiempo = self.tiempo + get_tiempo_vacio()
                    carguero = self.listaCargueros.getLibreSalida()
                    #TENDRIA QUE ASIGNARLE YA EL CARGUERO?

                    #Y AL CONTRARIO¿
                    # Oier: cuidado aqui, le estas asignando el iD de un 
                    # barco cuando el carguero viene vacio
                    self.listaCargueros.modificar(carguero[0],tiempo,sts.CARGUERO_DIRECCION_PUERTO,iD)
                    self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_VACIO,tiempo,carguero[0])      
        else:
            self.colaEntrada.addBarco(petrolero)   

    #Calculo si lanzo eventoMuellePuertoLleno o eventoMuellePuertoVacio y eventoDescarga.
    def eventoPuertoMuelleLleno(self, iD):
        #El evento descarga siempre se hace
        tiempoDescarga = self.tiempo + (60 * np.random.chisquare(self.grado_libertad_descarga))
        
        carguero = self.listaCargueros.getById(iD)
        iDPetrolero= carguero[3]
        
        self.listaPetroleros.modificar(carguero[3],tiempoDescarga,4,-1)
        self.listaCargueros.modificar(iD,tiempoDescarga, sts.CARGUERO_COLA_MUELLE,-1)
        
        #Estadistico muelles
        tiempo =tiempoDescarga-self.tiempo
        self.actualizarBarcosMuelle(tiempo)

        self.listaEventos.añadirEvento(sts.PETROLERO_DESCARGA,tiempoDescarga,iDPetrolero)
        #Si hay cola de salida
        #VUELVO LLENO
        if not self.listaMuelles.isEmpty():
            tiempoLleno = self.tiempo + get_tiempo_lleno()
            petrolero = self.listaMuelles.popBarcoEspera()

            #Estadistico muelles
            tiempoMuelle = self.tiempo - petrolero[1]
            self.actualizarBarcosMuelle(tiempoMuelle)

            self.listaCargueros.modificar(iD,tiempoLleno,3,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,3,iD)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,iD)

        # Si no hay colaSalida, si hay colaEntrada y hay muelles disponibles
        # VUELVO VACIO
        elif not self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoSolo = self.tiempo + get_tiempo_vacio()
            self.listaCargueros.modificar(iD,tiempoSolo,sts.CARGUERO_DIRECCION_PUERTO,-1)
            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoSolo,iD)
        
    
    #Calculo si lanzo eventoMuellePuertoLleno o ¿eventoMuellePuertoVacio?
    def eventoPuertoMuelleVacio(self, iD):
        self.listaCargueros.modificar(iD,self.tiempo,2,-1)
        #Vuelvo vacio
        #Si no hay cola salida y si la cola entrada.
        if self.listaMuelles.isEmpty() and not self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoSolo= self.tiempo + get_tiempo_vacio()
            self.listaCargueros.modificar(iD,tiempoSolo,sts.CARGUERO_DIRECCION_PUERTO,-1)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_VACIO,tiempoSolo,iD)
        #Vuelvo lleno
        #Si hay cola 
        elif not self.listaMuelles.isEmpty():
            tiempoLleno = self.tiempo + get_tiempo_lleno()
            petrolero = self.listaMuelles.popBarcoEspera()

            #Estadistico muelles
            tiempoMuelle = self.tiempo - petrolero[1]
            self.actualizarBarcosMuelle(tiempoMuelle)

            self.listaCargueros.modificar(iD,tiempoLleno, sts.CARGUERO_DIRECCION_PUERTO, petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,sts.CARGUERO_MUELLE_ENTRADA_LLENO,iD)

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,iD)

    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoLleno(self, iD):
        carguero = self.listaCargueros.getById(iD)
        self.listaPetroleros.modificar(carguero[3],carguero[1],6,-1)
        self.listaCargueros.modificar(iD,self.tiempo,sts.CARGUERO_COLA_ENTRADA,-1)
        

        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        if self.colaEntrada.isEmpty() and not self.listaMuelles.isEmpty():
            tiempoSolo= self.tiempo + get_tiempo_vacio()
            self.listaCargueros.modificar(iD,tiempoSolo,sts.CARGUERO_DIRECCION_MUELLE,-1)

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoSolo,iD)
        #Vuelvo lleno
        #Si hay cola y muelles
        elif not self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoLleno = self.tiempo + get_tiempo_lleno()
            numBarcosCola = self.colaEntrada.cola_entrada.qsize()
            petrolero = self.colaEntrada.popBarcoEspera()

             #Estadisticas
            tiempoAtraco = tiempoLleno - petrolero[1]
            tiempoEspera = self.tiempo - petrolero[1]

            self.actualizarEstadisticos(tiempoAtraco,tiempoEspera,numBarcosCola)

            self.listaCargueros.modificar(iD,tiempoLleno,sts.CARGUERO_DIRECCION_MUELLE,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno,sts.CARGUERO_ENTRADA_MUELLE_LLENO,iD)
            self.listaMuelles.addBarcoMuelle()

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempoLleno,iD)
    
    #Calculo si lanzo eventoPuertoMuelleLleno o eventoPuertoMuelleVacío.
    def eventoMuellePuertoVacio(self, iD):
        carguero = self.listaCargueros.getById(iD)
        self.listaCargueros.modificar(iD,self.tiempo,sts.CARGUERO_COLA_ENTRADA,-1)
        #Vuelvo vacio
        #Si no hay cola y si la cola salida.
        # Oier: No entiendo este if, si no hay nadie esperando a entrar y 
        # los muelles estan esperando a salir y hay cargueros esperando voy al muelle? 
        # Sera si estan esperando para salir no?
        if self.colaEntrada.isEmpty() and not self.listaMuelles.isEmpty():
            tiempoSolo = self.tiempo + get_tiempo_vacio()
            self.listaCargueros.modificar(iD,tiempoSolo,sts.CARGUERO_DIRECCION_MUELLE,-1)
            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoSolo,iD)

        #Si hay cola y muelles
        elif not self.colaEntrada.isEmpty() and self.listaMuelles.libre():
            tiempoLleno = self.tiempo + get_tiempo_lleno()
            numBarcosCola = self.colaEntrada.cola_entrada.qsize()
            petrolero = self.colaEntrada.popBarcoEspera()

            #Estadisticas
            tiempoAtraco = tiempoLleno - petrolero[1]
            tiempoEspera = self.tiempo - petrolero[1]
            self.actualizarEstadisticos(tiempoAtraco,tiempoEspera,numBarcosCola)

            self.listaCargueros.modificar(iD,tiempoLleno,sts.CARGUERO_DIRECCION_MUELLE,petrolero[0])
            self.listaPetroleros.modificar(petrolero[0],tiempoLleno, sts.CARGUERO_ENTRADA_MUELLE_LLENO, iD)
            self.listaMuelles.addBarcoMuelle()

            self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_LLENO,tiempoLleno,iD)
    
    #Calculo si lanzo eventoMuellePuertoLleno o meto en la cola o eventoPuertoMuelleVacio.
    def eventoDescarga(self, iD):
        self.listaPetroleros.modificar(iD,self.tiempo,sts.CARGUERO_COLA_MUELLE,-1)
        petrolero = self.listaPetroleros.getById(iD)

        if self.listaCargueros.libreSalida():
            carguero = self.listaCargueros.getLibreSalida()
            tiempoLleno = self.tiempo + get_tiempo_lleno()

            self.listaCargueros.modificar(carguero[0],tiempoLleno,sts.CARGUERO_DIRECCION_PUERTO,iD)
            self.listaPetroleros.modificar(iD,tiempoLleno,sts.CARGUERO_MUELLE_ENTRADA_LLENO,carguero[0])
            self.listaMuelles.eliminar()

            self.listaEventos.añadirEvento(sts.CARGUERO_MUELLE_ENTRADA_LLENO,tiempoLleno,carguero[0])
            #ASIGNO YA EL CARGUERO?

        else:
            self.listaMuelles.addBarcoEspera(petrolero)
            if self.listaCargueros.libreEntrada():
                carguero = self.listaCargueros.getLibreEntrada()
                tiempoVacio= self.tiempo + get_tiempo_vacio()
                self.listaCargueros.modificar(carguero[0],tiempoVacio,sts.CARGUERO_DIRECCION_MUELLE,-1)
                self.listaEventos.añadirEvento(sts.CARGUERO_ENTRADA_MUELLE_VACIO,tiempoVacio,carguero[0])


if __name__ == '__main__':
    simul = Main()
    simul.simular()

