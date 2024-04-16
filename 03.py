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
    # Excluimos la primera fila que contiene los encabezados
    rows = table.find_all("tr")[1:]

    # Lista para almacenar los registros
    registros = []

    # Iterar sobre las filas de la tabla
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            # Extraer los datos de cada celda
            rank = cells[0].text.strip()
            song = cells[1].text.strip()
            artist = cells[2].text.strip()
            weeks = cells[3].text.strip()
            country = cells[4].text.strip()
            # Agregar los datos del registro a la lista de registros
            registros.append({
                "Rank": rank,
                "Song": song,
                "Artist": artist,
                "Weeks": weeks,
                "Country": country,
            })

    # Convertir la lista de registros en un DataFrame de Pandas
    df = pd.DataFrame(registros)

    # Mostrar la tabla sin los países
    print("Tabla sin los países:")
    print(df.drop(columns=["Country"]))

    # Mostrar la tabla de artistas y países
    print("\nTabla de artistas y países:")
    print(df[["Artist", "Country"]])

else:
    print("Error al obtener la página:", response.status_code)
