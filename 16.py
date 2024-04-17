import sqlite3
import requests
from bs4 import BeautifulSoup


def principal():
    while True:
        print("\nMENU:")
        print("1.Obtener datos de la URL y alamcenar en la base de datos")
        print("2.Mostrar la base de datos")
        print("3.Consultar la cancion mas antigua ")
        print("4.Consultar el pais con mas canciones")
        print("5.Salir")
        eleccionn == input("Seleccione una opcion:  ")

        if eleccion == 1:
            obtener_y_almacenar_datos()
            print("Datos obtenidos y almacenados con exito!!!!")


ooo
