from random import randint

def entrenar(jugadas, rango_min, rango_max, iteraciones):
    #matriz de tuplas (valor, resultados positivos, intentos)
    for i in range(len(jugadas)):
        (val, pos, tot) = jugadas[i]
        for j in range(iteraciones):
            n = randint(rango_min,rango_max)
            n = n if n <= 10 else 10 # J,Q,K vale 10
            pos = pos if val+n > 21 else pos+1 
            tot = tot+1 
        jugadas[i] = (val, pos, tot)
    return jugadas

if __name__ == '__main__':
    jugadas = [
        (12,0,0), # Valor, intentos positivos, intentos negativos
        (13,0,0),
        (14,0,0),
        (15,0,0),
        (16,0,0),
        (17,0,0),
        (18,0,0),
        (19,0,0),
        (20,0,0),
    ]
    entrenar(jugadas, 1, 13, 1000000)
    print(jugadas)