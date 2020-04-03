#!/usr/bin/python
import xmlrpc.client
import argparse
import threading

def despliega_menu():
    print("MENU")
    print("1. Iniciar jugada")
    print("2. ¿Quiénes están jugando?")
    print("3. Crear partida") #Cambié mostrar partida por Crear partida, no se puede jugar si no se presiona 3 antes.
    print("4. jugar")
    print("6. Quiero otro nombre")
    print("0. Salir")
    o = input("Opcion:>")
    return int(o)

def jugada(proxy):
    j = proxy.agrega_jugador(jugador)
    print(j)

def cambiar_nombre():
    print("Actualmente te llamas {}".format(jugador))
    respuesta = safe_int("¿Desea cambiar de nombre? \n 0 - No \n 1 - Sí", 1)
    if respuesta == 1:
        nombre_viejo = jugador
        jugador = ""
        while jugador == "":
            jugador = input("Escribe tu nuevo nombre: (Nombre actual: {})".format(nombre_viejo))
        print("Bien, humano. Ahora te llamas: {}".format(jugador))

def safe_int( mensaje, opcion_max ):
    while True:
        respuesta = -1
        while respuesta < 0 or respuesta > opcion_max:
            try:
                respuesta = int(input(mensaje))
            except ValueError:
                print("Eso no es un número")
        return respuesta

def check_play( proxy ):
    while resultados == "":
        resultados = proxy.ver_resultado()
        if str(resultados) != "":
            print(resultados)

def main(jugador):
    vacio = True
    print("Iniciamos!")
    print("Primero crea tu jugada con 1")
    print("pica 3 para obtener todos los jugadores")
    print("pica 4 para iniciar el juego.")
    proxy = xmlrpc.client.ServerProxy('http://localhost:9000')
    thread1 = threading.Thread(target = check_play, args = (proxy,))
    thread1.start()
    try:
        opcion = 99
        while opcion != 0:
            opcion = despliega_menu()
            if opcion == 0: #Salir
                break
            if opcion == 1 and vacio == False: #Iniciar jugada
                cambiar_nombre()
                jugada(proxy) #Aquí se agrega al jugador si no está y se le da una mano.
            if opcion == 2: #Preguntar si hay más jugadores --> Imprime los jugadores que hay
                n = proxy.numero_jugadores()
                print( "Jugadores:",n )
            if opcion == 3: #Crear partida --> Me devuelve los jugadores que hay y sus manos.
                vacio = False
                d = proxy.deck()
                print(d)
            if opcion == 4: #jugar
                try:
                   ganador = ""
                   while True:
                        ganador = proxy.juez(d, proxy)
                        if len(ganador) == "":
                            print("EMPATE")
                            jugada(proxy)
                        else:
                            break
                except:
                    print("NO EXISTE PARTIDA")
            if opcion == 6: #cambiar nombre
                cambiar_nombre()
                
        print("Saliendo")

    except ConnectionError:
        print("Se desconecto el Server")
    except KeyboardInterrupt:
        print("Usuario cancela programa")


if __name__ == "__main__":
    parse =argparse.ArgumentParser()
    parse.add_argument("-j","--jugador",dest="jugador",required=False,default="El-cacas")
    args = parse.parse_args()
    jugador = args.jugador
    main(jugador)