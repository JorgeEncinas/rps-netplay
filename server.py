#!/usr/bin/python
# Integrantes del equipo:
#   Alcaraz Biebrich Manuel Alejandro
#   Encinas Alegre Jorge Carlos
#   Romero Andrade Paula Cristina
# Fecha: 3 de Abril de 2020
#
# Descripción de Modo de uso:
#  Se ejecuta este programa y se le mantiene de fondo antes de ejecutar cliente.py
#  Cada método describe su función particular.
#  Al iniciarse, el servidor registra las funciones que se utilizarán

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
    ''' Agrega un jugador al diccionario de j y devuelve su mano '''
    resultado = j.mano(jugador)
    print(resultado)
    return resultado

def numero_jugadores():
    ''' Regresa la cantidad de jugadores '''
    return len(j.jugadores)

def quitar_perdedores( delete_list ):
    ''' Recibe una lista con los jugadores perdedores y los quita del diccionario de jugadores. Regresa el nuevo diccionario.'''
    for key in delete_list:
        del j.jugadores[key]
    return j.jugadores

def deck():
    ''' Regresa el diccionario de jugadores '''
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
