import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import sqlite3

# Función para extraer datos desde una URL


def extraer_datos_desde_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            tabla = soup.find('table', {'class': 'wikitable'})
            html_str = str(tabla)
            datos = pd.read_html(html_str)[0]
            return datos
        else:
            print("Error al obtener el contenido de la URL:", response.status_code)
            return None
    except Exception as e:
        print("Error al extraer datos desde la URL:", e)
        return None

# Función para mostrar los datos


def mostrar_datos(datos):
    if datos is not None:
        print("Tabla de datos extraídos:")
        print(datos)
    else:
        print("No se han podido extraer datos.")

# Función para convertir la base de datos en una tabla


def convertir_bd_a_tabla(datos):
    try:
        if datos is not None and not datos.empty:
            print("Tabla de canciones:")
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
            print(
                "| ID |  Canción   |    Artista   | Semanas | Pais | Año    | Idioma | Continente|")
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
            for i, fila in datos.iterrows():
                print("| {:<2} | {:<10} | {:<12} | {:^7} | {:^4} | {:^6} | {:^5} | {:^9} |".format(
                    i+1, fila['Canción'], fila['Artista'], fila['Semanas'], fila['Pais'], fila['Año'], fila['Idioma'], fila['Continente']))
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
        else:
            print("La tabla de canciones está vacía.")
    except Exception as e:
        print("Error al convertir base de datos en tabla:", e)

# Función para agregar idioma y continente a cada registro


def agregar_idioma_continente(datos):
    if datos is not None and not datos.empty:
        idiomas_unicos = ['portugues', 'ingles',
                          'español', 'aleman', 'sueco', 'frances']
        continentes_unicos = ['europa', 'asia',
                              'america de sud', 'america de norte']
        for index, fila in datos.iterrows():
            print("\nRegistro:")
            print(fila)
            idioma = input(
                f"Ingrese el idioma para '{fila['Canción']}': ").lower()
            while idioma not in idiomas_unicos:
                print("Por favor, seleccione una opción válida.")
                idioma = input(
                    "Ingrese el idioma (portugues, ingles, español, aleman, sueco, frances): ").lower()
            continente = input(
                f"Ingrese el continente para '{fila['Canción']}': ").lower()
            while continente not in continentes_unicos:
                print("Por favor, seleccione una opción válida.")
                continente = input(
                    "Ingrese el continente (europa, asia, america de sud, america de norte): ").lower()
            datos.at[index, 'Idioma'] = idioma
            datos.at[index, 'Continente'] = continente
        print("Idioma y continente agregados correctamente.")
    else:
        print("Primero debe extraer los datos desde la URL.")

# Función para el menú de opciones


def menu():
    url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno"
    datos_extraidos = None

    while True:
        print("\nMENU:")
        print("1. Extraer y mostrar datos desde la URL")
        print("2. Agregar idioma y continente a cada registro")
        print("3. Crear tabla de canciones y mostrar")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            datos_extraidos = extraer_datos_desde_url(url)
            mostrar_datos(datos_extraidos)
        elif opcion == "2":
            agregar_idioma_continente(datos_extraidos)
        elif opcion == "3":
            convertir_bd_a_tabla(datos_extraidos)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


# Ejecutar el menú
menu()
