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
            datos = pd.read_html(StringIO(html_str))[0]
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


def convertir_bd_a_tabla():
    try:
        conn = sqlite3.connect('canciones.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canciones")
        filas = cursor.fetchall()
        if len(filas) > 0:  # Verificar si hay filas en la base de datos
            print("Tabla de canciones:")
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
            print(
                "| ID |  Canción   |    Artista   | Semanas | Pais | Año    | Idioma | Continente|")
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
            for i, fila in enumerate(filas, start=1):
                print("| {:<2} | {:<10} | {:<12} | {:^7} | {:^4} | {:^6} | {:^5} | {:^9} |".format(
                    i, fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
            print(
                "+----+------------+--------------+---------+------+--------+-------+-----------+")
        else:
            print("La base de datos está vacía.")
        conn.close()
    except Exception as e:
        print("Error al convertir base de datos en tabla:", e)
# Función para agregar idioma y continente a cada registro


def agregar_idioma_continente(datos):
    if datos is not None:
        idioma = input("Ingrese el idioma: ")
        continente = input("Ingrese el continente: ")
        datos['Idioma'] = idioma
        datos['Continente'] = continente
        print("Idioma y continente agregados correctamente.")
    else:
        print("Primero debe extraer los datos desde la URL.")

# Función para el menú de opciones


def menu():
    url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno"
    datos_extraidos = None

    while True:
        print("\nMENU:")
        print("1. Extraer datos desde la URL")
        print("2. Mostrar datos extraídos")
        print("3. Convertir base de datos en tabla")
        print("4. Agregar idioma y continente a cada registro")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if datos_extraidos is None:
                datos_extraidos = extraer_datos_desde_url(url)
                if datos_extraidos is not None:
                    print("Datos extraídos exitosamente.")
            else:
                print("Los datos ya han sido extraídos. Evitando duplicados.")
        elif opcion == "2":
            mostrar_datos(datos_extraidos)
        elif opcion == "3":
            convertir_bd_a_tabla()
        elif opcion == "4":
            agregar_idioma_continente(datos_extraidos)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


# Ejecutar el menú
menu()
