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

    # Mostrar todas las filas y celdas de la tabla
    for row in rows:
        cells = row.find_all(["th", "td"])
        for cell in cells:
            print(cell.text.strip(), end="\t")
        print()  # Agregar una nueva línea después de cada fila
else:
    print("Error al obtener la página:", response.status_code)
