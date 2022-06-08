from random import random, shuffle
import numpy as np


class Carta:
    palos = ['Picas', 'Corazones', 'Trebol', 'Diamantes']
    ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

    def __init__(self, orden):
        self.orden = orden
    
    def getPalo(self):
        return self.palos[int(self.orden / 13)]
    
    def getRank(self):
        return self.ranks[self.orden % 13]
    
    def toString(self):
        return "{} {}".format(self.getRank(), self.getPalo())

    def mostrar(self):
        print(self.toString())
    
    def valorCarta(self):
        if self.getRank() == 'A':
            return [1,11]
        elif self.getRank() == 'J' or self.getRank() == 'Q' or self.getRank() == 'K':
            return [10]
        else:
            return [int(self.getRank())]


class Mazo:
    def __init__(self, cant):
        self.cartas = []
        for i in range(cant):
            for j in range(52):
                self.cartas.append(Carta(j))
    
    def mezclar(self):
        shuffle(self.cartas)
    
    def toString(self):
        return [carta.toString() for carta in self.cartas]

    def mostrar(self):
        print(self.toString())

    def pop(self):
        return self.cartas.pop()
    
    def popMany(self, cant):
        if cant == 0:
            return []
        else:
            return self.popMany(cant-1).append(self.pop())
        

class Jugador: # QUEDA HACER LOS ARCHIVOS
    valores_jugada = [11,12,13,14,15,16,17,18,19,20] #Las posibles manos que puedo tener
    valores_croupier = [2,3,4,5,6,7,8,9,10,11]
    # Si mi jugada es <= 10 pido porque no me puedo pasar, si tengo 5 cartas o >=21 no puedo seguir.
    # Como el pago es 3 a 2, ganar de me da 0.5 y perder me saca 1 -> Para entero, ganar +1, perder -2
    def __init__(self, archivo, balance, randomness):
        if archivo:
            self.tabla_decision = archivo # Leo el archivo
        else:
            self.tabla_decision = np.zeros((3,10,10))
        self.jugada_actual = []
        self.randomness = randomness
        self.balance = balance

    def decisionActual(self,cartas,mispuntos,suspuntos,pide):
        self.jugada_actual.append([cartas,mispuntos,suspuntos,pide])
    
    def finCroupier(self,esVictoria):
        if(esVictoria):
            puntos=1
        else:
            puntos=-2
        for jugada in self.jugada_actual:
            self.tabla_decision[jugada[0]][jugada[1]][jugada[2]] = self.tabla_decision[jugada[0]][jugada[1]][jugada[2]] + puntos * jugada[3]
        self.jugada_actual = []

    def deseaPedir(self, cartas, mispuntos,suspuntos):
        cartas_ubic = self.valores_jugada.index(cartas)
        mispuntos_ubic = self.valores_jugada.index(mispuntos)
        suspuntos_ubic = self.valores_jugada.index(suspuntos)
        desea = (self.tabla_decision[cartas_ubic][mispuntos_ubic][suspuntos_ubic] + self.randomness * 2 * (random()-0.5)) >= 0 # Si es positivo pide. Si no, no. Agregamos random para que varie el comportamiento.
        return desea

    def guardarEntrenamiento(self,archivo):
        pass # Guardo el archivo

class Juego: ## TRABAJANDO EN ESTO
    def __init__(self, jugador, cant_mazos):
        self.jugador = jugador
        self.cant_mazos = cant_mazos
    
    def jugarMano(self):
        def puntos(cartas):
            puntos = 0
        mazo = Mazo(self.cant_mazos)
        cartas_jugador = mazo.popMany(2)
        cartas_croupier = mazo.popMany(1)
        #Modelar proceso de pedir cartas, y modificar la tabla segun resultado.


if __name__ == '__main__':
    mazo = Mazo(1)
    mazo.mostrar()
    mazo.mezclar()
    mazo.mostrar()

