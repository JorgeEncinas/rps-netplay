#!/usr/bin/python
import xmlrpc.client
import argparse

def despliega_menu():
    print("MENU")
    print("1.Iniciar jugada")
    print("2.Preguntar si hay más jugadores")
    print("3.Crear partida") #Cambie mostrar partida por Crear partida, no se puede jugar si no se presiona 3 antes.
    print("4.jugar")
    print("0.Salir")
    o = input("Opcion:>")
    return int(o)

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


def juez(jugadores, proxy):
    #en el diccionario el nombre del jugador se representa como j y su jugada es jugadores[j])
    tuplas=jugadores.items()
    participes=[]
    for j in tuplas:
        participes.append(j)
    winner=RPS(participes[0], participes[1])
    #Para juegos de muchos jugadores  se podria llamar RPS dentro de un loop????
    print("EL GANADOR ES... ", winner)

    if (winner=="EMPATE"):
    #llama a jugada para que le de una nueva mano al jugador
        jugada(proxy)

def jugada(proxy):
    j=proxy.agrega_jugador(jugador)
    print(j)

def main(jugador):
    print("Iniciamos!")
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    try:
        opcion = 99
        while opcion != 0:
            opcion = despliega_menu()
            if opcion == 0:
                break
            if opcion == 1:
                jugada(proxy)

            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:",n)
            if opcion == 3:
                d = proxy.deck()
                print(d)
            if opcion == 4:
                try:
                    juez(d,proxy)
                except:
                    print("NO EXISTE PARTIDA")
        print("Saliendo")

    except ConnectionError:
        print("Se desconecto el Server")
    except KeyboardInterrupt:
        print("Usuario cancela programa")


if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-j","--jugador",dest="jugador",required=False,default="Fede")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)