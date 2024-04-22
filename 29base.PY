import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import sqlite3


def extraer_datos_desde_url(url):
    try:
        # Realizar la solicitud GET a la URL
        response = requests.get(url)
        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Especificar la codificación como utf-8 al decodificar el contenido de la respuesta
            response.encoding = 'utf-8'
            # Parsear el contenido HTML de la respuesta
            soup = BeautifulSoup(response.text, 'html.parser')
            # Encontrar la tabla en la página
            tabla = soup.find('table', {'class': 'wikitable'})
            # Extraer los datos de la tabla
            html_str = str(tabla)
            # Utilizar StringIO para evitar la advertencia
            datos = pd.read_html(StringIO(html_str))[0]
            return datos
        else:
            print("Error al obtener el contenido de la URL:", response.status_code)
            return None
    except Exception as e:
        print("Error al extraer datos desde la URL:", e)
        return None


def mostrar_datos(datos):
    if datos is not None:
        print("Tabla de datos extraídos:")
        print(datos)
    else:
        print("No se han podido extraer datos.")


def convertir_bd_a_tabla():
    try:
        conn = sqlite3.connect('canciones.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canciones")
        filas = cursor.fetchall()
        print("Tabla de canciones:")
        print("+----+------------+--------------+---------+------+--------+")
        print("| ID |  Canción   |    Artista   | Semanas | Pais | Año    |")
        print("+----+------------+--------------+---------+------+--------+")
        for i, fila in enumerate(filas, start=1):
            print("| {:<2} | {:<10} | {:<12} | {:^7} | {:^4} | {:^6} |".format(
                i, fila[0], fila[1], fila[2], fila[3], fila[4]))
        print("+----+------------+--------------+---------+------+--------+")
        conn.close()
    except Exception as e:
        print("Error al convertir base de datos en tabla:", e)


def menu():
    url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno"
    datos_extraidos = None  # Inicializar los datos extraídos como None

    while True:
        print("\nMENU:")
        print("1. Extraer datos desde la URL")
        print("2. Mostrar datos extraídos")
        print("3. Convertir base de datos en tabla")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if datos_extraidos is None:  # Verificar si los datos ya han sido extraídos
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
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


if __name__ == "__main__":
    menu()
