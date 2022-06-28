from random import random, shuffle

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
            return 11
        elif self.getRank() == 'J' or self.getRank() == 'Q' or self.getRank() == 'K':
            return 10
        else:
            return int(self.getRank())

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
            return self.popMany(cant-1) + [self.pop()]

class Jugador: ########## HAY QUE DEFINIR QUE HACEMOS CUANDO TENEMOS UN A LIBRE, COMO A9 que es buena mano y tal vez no deberia pedir
    def __init__(self, porcentaje_decision, balance, apuesta_por_mano, tipo_apuesta):
        def deboPedir(tupla):
            (val,pos,tot) = tupla
            return (val, (pos/tot) >= porcentaje_decision)
        
        self.jugadas = [
            (12, 692148, 1000000), 
            (13, 615085, 1000000), 
            (14, 539663, 1000000), 
            (15, 460911, 1000000), 
            (16, 384851, 1000000), 
            (17, 308139, 1000000), 
            (18, 230360, 1000000), 
            (19, 154351, 1000000), 
            (20, 77015, 1000000)
        ]

        self.decision = [deboPedir(jugada) for jugada in self.jugadas]
        self.balance_inicial = balance
        self.balance = balance
        self.apuesta_por_mano = apuesta_por_mano
        self.tipo_apuesta = tipo_apuesta
        self.estadisticas = {"jugados": 0, "ganados": 0, "empatados": 0, "perdidos": 0, "blackjack": 0, "maxcartas": 0}
    
    def tieneFichas(self):
        return self.balance > 0
    
    def getApuesta(self):
        apuesta_minima = 10
        apuesta_por_mano = self.apuesta_por_mano
        tipo_apuesta = self.tipo_apuesta

        if self.balance < apuesta_minima:
            val = self.balance
        elif tipo_apuesta == "FIJO":
            val = apuesta_por_mano if self.balance >= apuesta_por_mano else self.balance
        else:
            val = apuesta_por_mano * self.balance if self.balance >= apuesta_por_mano * self.balance else self.balance

        self.balance = self.balance - val
        return val
    
    def pagar(self, fichas):
        self.balance = self.balance + fichas

    def deseaPedir(self, mispuntos): # POR EL MOMENTO SOLO ME INTERESA EL PUNTAJE MAXIMO
        if mispuntos >= 21:
            return False
        for (val, desea) in self.decision:
            if val == mispuntos:
                return desea
        return True # Tengo maximo 11, no me puedo pasar
    
    def agregarEstadisticas(self, etiquetas):
        for etiqueta in etiquetas:
            self.estadisticas[etiqueta] = self.estadisticas[etiqueta] + 1

    def informe(self):
        print("INFORME DEL JUGADOR")
        print("Balance inicial: " + str(self.balance_inicial))
        print("Balance actual: " + str(self.balance))
        print("Manos jugadas: " + str(self.estadisticas["jugados"]))
        print("Manos ganadas: " + str(self.estadisticas["ganados"]))
        print("Manos empatadas: " + str(self.estadisticas["empatados"]))
        print("Manos perdidas: " + str(self.estadisticas["perdidos"]))
        print("Manos con blackjack: " + str(self.estadisticas["blackjack"]))
        print("Manos con 5 cartas: " + str(self.estadisticas["maxcartas"]))

class Juego: ## TRABAJANDO EN ESTO
    def __init__(self, jugador, cant_mazos):
        self.jugador = jugador
        self.cant_mazos = cant_mazos
        self.historia_jugadas = []

    def informarMano(self, nro_mano):
        print(str(self.historia_jugadas[nro_mano]))
    
    def informarManos(self):
        print("INFORME DE MANOS")
        for i in range(len(self.historia_jugadas)):
            print("=== MANO {} ===".format(i+1))
            self.informarMano(i)

    def jugarManos(self, cant):
        [self.jugarMano() for i in range(cant)]
    
    def jugarMano(self):
        def puntosMax(cartas): #ACA YA MANEJO EL PROBLEMA CON LOS ASES, JUEGO A LA SEGURA Y NO PIDO MAS
            puntos = 0
            for carta in cartas:
                puntos = puntos + carta.valorCarta()
            if puntos >= 21:
                for carta in cartas:
                    if puntos > 21 and carta.getRank() == 'A':
                        puntos = puntos - 10
            return puntos
        
        def puntosMin(cartas): #ACA YA MANEJO EL PROBLEMA CON LOS ASES, JUEGO AL RIESGO, SI ME PASO NO PERDI
            puntos = 0
            for carta in cartas:
                puntos = puntos + carta.valorCarta()
                if carta.getRank() == 'A':
                    puntos = puntos - 10
            return puntos
        
        def esBlackJack(cartas):
            return puntosMax(cartas) == 21 and len(cartas) == 2

        def esMaxCartas(cartas):
            return len(cartas) == 5

        def comparar(cartas_jugador, cartas_croupier):
            etiquetas = ["jugados"]
            ganancia_porcentual = 0.0
            if esBlackJack(cartas_jugador):
                etiquetas.append("blackjack")
                if esBlackJack(cartas_croupier):
                    etiquetas.append("empatados")
                    ganancia_porcentual = 1.0
                else:
                    etiquetas.append("ganados")
                    ganancia_porcentual = 2.0
            elif esMaxCartas(cartas_jugador) and not esBlackJack(cartas_croupier):
                etiquetas.append("maxcartas")
                if esMaxCartas(cartas_croupier):
                    etiquetas.append("empatados")
                    ganancia_porcentual = 1.0
                else:
                    etiquetas.append("ganados")
                    ganancia_porcentual = 1.5
            else:
                if not (esBlackJack(cartas_croupier) or esMaxCartas(cartas_croupier)):
                    if puntosMax(cartas_jugador) > puntosMax(cartas_croupier):
                        etiquetas.append("ganados")
                        ganancia_porcentual = 1.5
                    elif puntosMax(cartas_jugador) == puntosMax(cartas_croupier):
                        etiquetas.append("empatados")
                        ganancia_porcentual = 1
                    else:
                        etiquetas.append("perdidos")
                else:
                    etiquetas.append("perdidos")
            # Devuelvo una tupla con la ganancia a devolver
            return(ganancia_porcentual, etiquetas)



        mazo = Mazo(self.cant_mazos)
        mazo.mezclar()

        if jugador.tieneFichas():
            apuesta = jugador.getApuesta()

            cartas_jugador = mazo.popMany(2)
            cartas_croupier = mazo.popMany(1)
            
            # Tengo 2 cartas, juego yo
            desea = True
            while jugador.deseaPedir(puntosMax(cartas_jugador)) and not esMaxCartas(cartas_jugador):
                cartas_jugador.append(mazo.pop())

            #Juega Croupier
            while puntosMax(cartas_croupier) < 17 and not esMaxCartas(cartas_croupier): # Si o si pido la segunda carta, porque A vale 11
                cartas_croupier.append(mazo.pop())

            (ganancia, etiquetas) = comparar(cartas_jugador, cartas_croupier)
            # Devuelve un listado del diccionario con las etiquetas
            # Se corresponde con
            # self.estadisticas = {"jugados": 0, "ganados": 0, "empatados": 0, "perdidos": 0, "blackjack": 0, "maxcartas": 0}
            
            jugador.pagar(int(apuesta * ganancia))
            jugador.agregarEstadisticas(etiquetas)

            self.historia_jugadas.append({
                "apuesta": apuesta, 
                "ganancia": int(apuesta * ganancia), 
                "cartas_croupier": [c.getRank() for c in cartas_croupier],
                "cartas_jugador": [c.getRank() for c in cartas_jugador]
            })

        # else:
        #     print('El jugador no tiene dinero.')

if __name__ == '__main__':
    print("JUGADOR 1")
    jugador = Jugador(0,3000,0.010,"PORCENTUAL") # Juega solo si esta seguro (0 prob de error), comienza con 3000 fichas. Apuesta el 1% por mano
    juego = Juego(jugador,1) #Jugamos con nuestro jugador, con 1 mazo
    juego.jugarManos(10000)
    jugador.informe()
    #juego.informarManos()
    print()
    print("JUGADOR 2")
    jugador = Jugador(0,3000,300,"FIJO") # Juega solo si esta seguro (0 prob de error), comienza con 3000 fichas. Apuesta 300 por mano, de forma fija
    juego = Juego(jugador,1) #Jugamos con nuestro jugador, con 1 mazo
    juego.jugarManos(10000)
    jugador.informe()
    #juego.informarManos()

    #Para el trabajo, hacer comparacion para definir cerrar en 0 la probabilidad necesaria. Luego, para definir usar fijo o porcentual, usar laa comparativa y explicar por que pasa. Usar estadisticas (min,max,media, distribucion)

    # jugador = Jugador(0,100,10,"FIJO") # Juega si tiene 2/3 de chances, comienza con 100 fichas. Apuesta 10 por mano, de forma fija
    # juego = Juego(jugador,1) #Jugamos con nuestro jugador, con 1 mazo
    # juego.jugarManos(1000)
    # jugador.informe()
    # #juego.informarManos()



