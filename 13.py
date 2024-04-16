import pandas as pd
import json
import tkinter as tk
import os
import requests
from bs4 import BeautifulSoup


def obtener_datos_json():
    # Verificar si el archivo JSON ya existe
    if os.path.exists("canciones.json"):
        # Leer el archivo JSON
        with open("canciones.json", "r", encoding="utf-8") as json_file:
            datos_json = json.load(json_file)
    else:
        datos_json = []

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

                # Verificar si el registro ya está en la lista
                if {"Título": titulo, "Intérprete": interprete, "Año": año, "Semanas": semanas, "País": pais} not in datos_json:
                    # Agregar los datos del registro a la lista de registros
                    registros.append({
                        "Título": titulo,
                        "Intérprete": interprete,
                        "Año": año,
                        "Semanas": semanas,
                        "País": pais
                    })

        # Agregar nuevos registros a la lista existente
        datos_json.extend(registros)

        # Guardar los datos en un archivo JSON
        with open("canciones.json", "w", encoding="utf-8") as json_file:
            json.dump(datos_json, json_file, ensure_ascii=False, indent=4)

        print("Datos guardados en canciones.json.")
    else:
        print("Error al obtener la página:", response.status_code)


def convertir_json_a_tabla():
    # Leer el archivo JSON
    with open("canciones.json", "r", encoding="utf-8") as json_file:
        datos_json = json.load(json_file)

    # Convertir los datos en un DataFrame de Pandas
    df = pd.DataFrame(datos_json)

    # Mostrar el DataFrame (aquí lo he imprimido en la consola, pero puedes mostrarlo en una ventana de la interfaz gráfica si deseas)
    print(df)


def acceder_a_url_y_convertir():
    obtener_datos_json()
    convertir_json_a_tabla()


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Obtener Datos y Convertir")

# Crear botón para acceder a la URL y convertir datos
boton_url_json_tabla = tk.Button(
    ventana, text="Acceder a la URL y Convertir a JSON y Tabla", command=acceder_a_url_y_convertir)
boton_url_json_tabla.pack(pady=10)

# Crear botón para convertir JSON a tabla
boton_json_tabla = tk.Button(
    ventana, text="Convertir JSON a Tabla", command=convertir_json_a_tabla)
boton_json_tabla.pack(pady=10)

# Ejecutar el bucle principal de la interfaz gráfica
ventana.mainloop()
