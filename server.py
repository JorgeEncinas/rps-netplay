#!/usr/bin/python
from xmlrpc.server import SimpleXMLRPCServer
import logging
import random

class Juego:
    jugadores = None
    opciones = None

    def __init__(self):
        self.jugadores = {}
        self.opciones = ['Piedra', 'Papel', 'Tijera']

    def mano(self, jugador):
        i = random.randint(0, 2)
        self.jugadores[jugador] = self.opciones[i]
        return [jugador, self.opciones[i]]

# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
    )
j = Juego()

def ver_resultado():
    return resultados

def juez( jugadores, proxy ):
    #en el diccionario el nombre del jugador se representa como j y su jugada es jugadores[j])
    tuplas = jugadores.items()
    participes=[]
    for j in tuplas:
        participes.append(j)
    winner=RPS(participes[0], participes[1])
    #Para juegos de muchos jugadores  se podria llamar RPS dentro de un loop????
    ganador = "EL GANADOR ES... {}".format(winner)

    if (winner=="EMPATE"):
        ganador = ""
    else:
        jugadaTerminada = True
    resultados = ganador
    return ganador

#def judgement_time( jugadores, proxy ):

def RPS(manita, manota):
    ganador=""
    if (manita[1]==manota[1]): ganador="EMPATE"

    if (manita[1] == 'Piedra' and manota[1] == 'Papel'): ganador = manota[0]
    if (manita[1] == 'Piedra' and manota[1] == 'Tijera'): ganador = manita[0]

    if (manita[1] == 'Papel' and manota[1] == 'Piedra'): ganador = manita[0]
    if (manita[1] == 'Papel' and manota[1] == 'Tijera'): ganador = manota[0]

    if (manita[1] == 'Tijera' and manota[1] == 'Piedra'): ganador = manota[0]
    if (manita[1] == 'Tijera' and manota[1] == 'Papel'): ganador = manita[0]

    return ganador

def agrega_jugador(jugador):
    resultado = j.mano(jugador)
    print(resultado)
    return resultado

def numero_jugadores():
    return len(j.jugadores)

def deck():
    return j.jugadores

def main():
    server.register_function(agrega_jugador)
    server.register_function(numero_jugadores)
    server.register_function(deck)
    server.register_function(juez)
    resultados = ""
    jugadaTerminada = False
    # Start the server
    try:
        print('Usa Control-C para salir')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')


if __name__ == "__main__":
    main()
