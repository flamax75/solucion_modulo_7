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


def cancion_mas_antigua():
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM canciones ORDER BY año ASC LIMIT 1')
    fila = cursor.fetchone()
    if fila:
        print(
            f"La canción más antigua es '{fila[0]}' de {fila[1]}, del año {fila[2]}.")
    else:
        print("No hay canciones registradas en la base de datos.")
    conexion.close()


def pais_con_mas_canciones():
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT pais, COUNT(*) as total
        FROM (
            SELECT SUBSTR(pais, 1, INSTR(pais, '/') - 1) as pais
            FROM canciones
            WHERE pais LIKE '%/%'
            UNION ALL
            SELECT pais
            FROM canciones
            WHERE pais NOT LIKE '%/%'
        )
        GROUP BY pais
        ORDER BY total DESC
        LIMIT 1
    ''')
    resultado = cursor.fetchone()
    if resultado:
        print(
            f"El país con más canciones es {resultado[0]} con {resultado[1]} canciones.")
    else:
        print("No hay suficientes datos para determinar el país con más canciones.")
    conexion.close()


def convertir_datos():
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canciones_convertidas (
            cancion TEXT,
            artista TEXT,
            año TEXT,
            semanas_en_numero_uno INTEGER,
            pais TEXT,
            UNIQUE(cancion, artista, año)
        )
    ''')

    cursor.execute('SELECT * FROM canciones')
    filas = cursor.fetchall()
    for fila in filas:
        cancion = fila[0]
        artista = fila[1]
        año = fila[2].split('/')[0]  # Tomar solo el primer año
        semanas = fila[3]
        pais = fila[4].split('/')[0]  # Tomar solo el primer país
        cursor.execute('INSERT OR IGNORE INTO canciones_convertidas (cancion, artista, año, semanas_en_numero_uno, pais) VALUES (?, ?, ?, ?, ?)',
                       (cancion, artista, año, semanas, pais))
    conexion.commit()
    conexion.close()
    print("Datos convertidos y almacenados en una nueva tabla 'canciones_convertidas'.")


def principal():
    while True:
        print("\nMenú:")
        print("1. Obtener datos de la URL y almacenar en la base de datos")
        print("2. Mostrar base de datos")
        print("3. Consultar la canción más antigua")
        print("4. Consultar el país con más canciones")
        print("5. Convertir datos (mostrar solo primer año y primer país)")
        print("6. Salir")
        eleccion = input("Ingrese su elección: ")

        if eleccion == '1':
            obtener_y_almacenar_datos()
            print("Datos obtenidos y almacenados con éxito.")
        elif eleccion == '2':
            mostrar_base_de_datos()
        elif eleccion == '3':
            cancion_mas_antigua()
        elif eleccion == '4':
            pais_con_mas_canciones()
        elif eleccion == '5':
            convertir_datos()
        elif eleccion == '6':
            print("Saliendo...")
            break
        else:
            print("Elección inválida. Por favor, ingrese un número del 1 al 6.")


if __name__ == '__main__':
    principal()
