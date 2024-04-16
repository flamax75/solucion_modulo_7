import requests
from bs4 import BeautifulSoup
import sqlite3


def obtener_y_almacenar_datos():
    url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno'
    respuesta = requests.get(url)
    sopa = BeautifulSoup(respuesta.text, 'html.parser')
    tabla = sopa.find('table', {'class': 'wikitable'})

    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canciones (
            cancion TEXT,
            artista TEXT,
            año TEXT,
            semanas_en_numero_uno INTEGER,
            pais TEXT,
            UNIQUE(cancion, artista, año)
        )
    ''')

    for fila in tabla.find_all('tr')[1:]:
        celdas = fila.find_all('td')
        if len(celdas) > 4:
            cancion = celdas[0].text.strip()
            artista = celdas[1].text.strip()
            # Extrae el primer año en caso de un rango
            año = celdas[2].text.strip().split('/')[0]
            semanas = int(celdas[3].text.strip())
            pais = celdas[4].text.strip()
            cursor.execute('INSERT OR IGNORE INTO canciones (cancion, artista, año, semanas_en_numero_uno, pais) VALUES (?, ?, ?, ?, ?)',
                           (cancion, artista, int(año), semanas, pais))  # Convierte el año a entero
    conexion.commit()
    conexion.close()


def mostrar_base_de_datos():
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM canciones')
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)
    conexion.close()


def principal():
    while True:
        print("\nMenú:")
        print("1. Obtener datos de la URL y almacenar en la base de datos")
        print("2. Mostrar base de datos")
        print("3. Salir")
        eleccion = input("Ingrese su elección: ")

        if eleccion == '1':
            obtener_y_almacenar_datos()
            print("Datos obtenidos y almacenados con éxito.")
        elif eleccion == '2':
            mostrar_base_de_datos()
        elif eleccion == '3':
            print("Saliendo...")
            break
        else:
            print("Elección inválida. Por favor, ingrese 1, 2 o 3.")


if __name__ == '__main__':
    principal()
