import requests
from bs4 import BeautifulSoup
import sqlite3


def extraer_resultados(url):
    conn = sqlite3.connect('canciones.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='canciones'")
    if cursor.fetchone()[0] == 1:
        print("Los datos ya han sido extraídos y guardados en la base de datos.")
        conn.close()
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la tabla que contiene los datos
    tabla = soup.find('table', {'class': 'wikitable'})

    # Extraer los datos de la tabla
    filas = tabla.find_all('tr')[1:]  # Ignoramos la primera fila (encabezados)

    resultados = []
    for fila in filas:
        columnas = fila.find_all('td')
        cancion = columnas[0].text.strip()
        artista = columnas[1].text.strip()
        semanas = int(columnas[3].text.strip())
        año = columnas[4].text.strip()
        pais = columnas[2].text.strip()
        resultados.append((cancion, artista, semanas, año, pais))

    cursor.execute('''CREATE TABLE IF NOT EXISTS canciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cancion TEXT,
                    artista TEXT,
                    semanas INTEGER,
                    año TEXT,
                    pais TEXT
                )''')

    ccursor.executemany(
        "INSERT INTO canciones (cancion, artista, semanas, año, pais) VALUES (?, ?, ?, ?, ?)", resultados)

    conn.commit()
    conn.close()

    print("Datos extraídos y guardados en la base de datos.")


def mostrar_datos_desde_bd():
    conn = sqlite3.connect('canciones.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM canciones")
    filas = cursor.fetchall()

    print("Canciones:")
    for fila in filas:
        print(fila)

    conn.close()


def convertir_bd_a_tabla():
    conn = sqlite3.connect('canciones.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM canciones")
    filas = cursor.fetchall()

    print("Tabla de canciones:")
    print("+------------+--------------+---------+------+--------+\n|  Canción   |    Artista   | Semanas | País  | Año    |\n+------------+--------------+---------+------+--------+\n")
    for fila in filas:
        print("| {:<11} | {:<12} | {:^7} | {:^6} | {:^4} |".format(
            fila[0], fila[1], fila[2], fila[3], fila[4]))
    print("+------------+--------------+---------+------+--------+")

    conn.close()


def menu():
    url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno"

    while True:
        print("\nMENU:")
        print("1. Extraer resultados de la URL y guardar en base de datos")
        print("2. Mostrar datos desde la base de datos")
        print("3. Convertir base de datos en tabla y mostrar")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            extraer_resultados(url)
        elif opcion == "2":
            mostrar_datos_desde_bd()
        elif opcion == "3":
            convertir_bd_a_tabla()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


if __name__ == "__main__":
    menu()
