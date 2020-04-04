#!/usr/bin/python
import xmlrpc.client
import argparse

def despliega_menu():
    print("MENU")
    print("1. Iniciar jugada")
    print("2. Preguntar si hay más jugadores")
    print("3. Crear partida") #Cambie mostrar partida por Crear partida, no se puede jugar si no se presiona 3 antes.
    print("4. jugar")
    print("5. Cambiar Nombre")
    print("0. Salir")
    o = input("Opcion:>")
    return int(o)

def cambiar_nombre( jugador ):
    print("Actualmente te llamas {}".format(jugador))
    respuesta = safe_int("¿Desea cambiar de nombre? \n 0 - No \n 1 - Sí \n", 1)
    if respuesta == 1:
        nombre_viejo = jugador
        jugador = ""
        while jugador == "":
            jugador = input("Escribe tu nuevo nombre: (Nombre actual: {}) \n".format(nombre_viejo))
        print("Bien, humano. Ahora te llamas: {} \n".format(jugador))
    return jugador

def safe_int( mensaje, opcion_max ):
    while True:
        respuesta = -1
        while respuesta < 0 or respuesta > opcion_max:
            try:
                respuesta = int(input(mensaje))
            except ValueError:
                print("Eso no es un número")
        return respuesta

def gen_game_data( jugadores, proxy, primera_vez ): # d = jugadores = proxy.deck() = j.jugadores = dict
    print("Generando datos!")
    if not primera_vez:
        for k, v in jugadores.items():
            jugada(proxy, k)
            jugadores = proxy.deck()
    tuplas=jugadores.items()
    participes=[]
    dict_survivors = dict()
    for j in tuplas:
        participes.append(j)
        dict_survivors[j[0]] = 1
    return participes, dict_survivors

def judgement_time( proxy, participes, dict_survivors ):
    print("Judgement Time!")
    for player in participes:
        for opponent in participes[1:]:
            if dict_survivors[opponent[0]] > 0 and player[0] != opponent[0]:
                print("Entrando a los chingazos!")
                RPS2(player, opponent, dict_survivors)
                print(dict_survivors)
    hay_ganador, ganador, jugadores = buscar_ganador( dict_survivors, proxy )
    print("El valor de hay ganador es: {}".format(hay_ganador))
    if hay_ganador == 1:
        print("EL GANADOR ES... ", ganador)
    elif hay_ganador == 2:
        participes, dict_survivors = gen_game_data( jugadores, proxy, False )
        judgement_time( proxy, participes, dict_survivors)
    elif hay_ganador == 0:
        print("EMPATE")
    else:
        print("El que programó esta función es tonto chaval tío")

def buscar_ganador( dict_survivors, proxy ):
    print("Buscando ganador!")
    ganador = ""
    delet_this = []
    hay_ganador = -1
    for k, v in dict_survivors.items():
        if v < 1:
            delet_this.append(k)
    dict_jugrest = proxy.quitar_perdedores(delet_this)
    print("\n Jugadores Restantes")
    print(dict_jugrest)
    if len( dict_jugrest ) > 1:
        print("Más de un jugador ganó!")
        hay_ganador = 2
    elif len( dict_jugrest ) == 1:
        print("Alguien ganó!")
        hay_ganador = 1
        for k, v in dict_jugrest.items():
            ganador = k
    else:
        hay_ganador = 0
    return hay_ganador, ganador, dict_jugrest

def RPS2(manita, manota, dict_survivors):
    print("Se enfrentan {} con {} contra {} con {}".format(manita[0], manita[1], manota[0], manota[1]))
    if (manita[1] == 'Piedra' and manota[1] == 'Papel'):
        dict_survivors[manita[0]] -=1
        print("{} se hizo pedazos a {}".format(str(manota[0]), str(manita[0])))
    if (manita[1] == 'Piedra' and manota[1] == 'Tijera'):
        dict_survivors[manota[0]] -=1
        print("{} se hizo pedazos a {}".format(str(manita[0]), str(manota[0])))

    if (manita[1] == 'Papel' and manota[1] == 'Piedra'):
        dict_survivors[manota[0]] -=1
        print("{} se hizo pedazos a {}".format(str(manota[0]), str(manita[0])))
    if (manita[1] == 'Papel' and manota[1] == 'Tijera'):
        dict_survivors[manita[0]] -=1
        print("{} se hizo pedazos a {}".format(str(manita[0]), str(manota[0])))

    if (manita[1] == 'Tijera' and manota[1] == 'Piedra'):
        dict_survivors[manita[0]] -= 1
        print("{} se hizo pedazos a {}".format(str(manota[0]), str(manita[0])))
    if (manita[1] == 'Tijera' and manota[1] == 'Papel'):
        dict_survivors[manota[0]] -= 1
        print("{} se hizo pedazos a {}".format(str(manita[0]), str(manota[0])))

def jugada(proxy, jugador):
    j=proxy.agrega_jugador(jugador)
    print(j)

def main(jugador):
    print("Iniciamos!")
    print("Primero crea tu jugada con 1")
    print("pica 3 para obtener todos los jugadores")
    print("pica 4 para iniciar el juego.")
    creado = False
    nombre_selected = False
    if jugador != "El-Cacas":
        nombre_selected = True
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    try:
        opcion = 99
        while opcion != 0:
            opcion = despliega_menu()
            if opcion == 0:
                break
            if opcion == 1:
                if nombre_selected == False:
                    jugador = cambiar_nombre( jugador )
                    nombre_selected = True
                jugada(proxy, jugador)
                creado = True
            if opcion == 2:
                n = proxy.numero_jugadores()
                print("Jugadores:",n)
            if opcion == 3:
                if creado == True:
                    d = proxy.deck()
                    print(d)
                else:
                    print("No has creado tu mano. Presiona 1.")
            if opcion == 4:
                #try:
                participes, dict_survivors = gen_game_data( d, proxy, True)
                judgement_time( proxy, participes, dict_survivors )
                #except:
                #    print("NO EXISTE PARTIDA")
            if opcion == 5:
                if nombre_selected == False:
                    jugador = cambiar_nombre( jugador )
                    nombre_selected = True
                else:
                    print("Tu nombre ya ha sido decidido.")
        print("Saliendo")

    except ConnectionError:
        print("Se desconecto el Server")
    except KeyboardInterrupt:
        print("Usuario cancela programa")


if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-j","--jugador",dest="jugador",required=False,default="El-Cacas")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)