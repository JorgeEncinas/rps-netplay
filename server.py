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

def agrega_jugador(jugador):
    resultado = j.mano(jugador)
    print(resultado)
    return resultado

def numero_jugadores():
    return len(j.jugadores)

def limpiar_jugadores():
    for k, v in list(j.jugadores):
        del jugadores[k]

def quitar_perdedores( delete_list ):
    for key in delete_list:
        del j.jugadores[key]
    return j.jugadores

def deck():
    return j.jugadores

def main():
    server.register_function(agrega_jugador)
    server.register_function(numero_jugadores)
    server.register_function(deck)
    server.register_function(quitar_perdedores)
    # Start the server
    try:
        print('Usa Control-C para salir')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')


if __name__ == "__main__":
    main()
