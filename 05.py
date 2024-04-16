import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL de la página de Wikipedia
url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno"

# Realizar la solicitud HTTP
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar la tabla con las canciones
    table = soup.find("table", {"class": "wikitable"})

    # Identificar los registros (filas) de la tabla
    rows = table.find_all("tr")

    # Lista para almacenar los registros
    registros = []

    # Iterar sobre las filas de la tabla
    for row in rows:
        cells = row.find_all(["th", "td"])
        if len(cells) > 0:
            # Extraer los datos de cada celda
            titulo = cells[0].text.strip()
            interprete = cells[1].text.strip()
            año = cells[2].text.strip()
            semanas = cells[3].text.strip()
            pais = cells[4].text.strip()  # Nueva columna para el país

            # Agregar los datos del registro a la lista de registros
            registros.append((titulo, interprete, año, semanas, pais))

    # Crear una conexión a la base de datos SQLite
    conn = sqlite3.connect("canciones.db")

    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

    # Crear una tabla para almacenar las canciones
    cursor.execute('''CREATE TABLE IF NOT EXISTS canciones (
                        titulo TEXT,
                        interprete TEXT,
                        año TEXT,
                        semanas TEXT,
                        pais TEXT
                    )''')

    # Insertar los registros en la tabla de canciones
    cursor.executemany(
        "INSERT INTO canciones VALUES (?, ?, ?, ?, ?)", registros)

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()

    print("Datos almacenados en la base de datos SQLite.")
else:
    print("Error al obtener la página:", response.status_code)
