import requests
from bs4 import BeautifulSoup
import sqlite3

# URL de la página a acceder
url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno'

# Conexión a la base de datos SQLite
conn = sqlite3.connect('songs.db')
c = conn.cursor()

# Crear tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        artist TEXT,
        song TEXT,
        weeks_at_number_one INTEGER,
        UNIQUE(artist, song)
    )
''')

# Obtener el contenido de la página
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Analizar la tabla específica
table = soup.find('table', {'class': 'wikitable'})

# Extraer y almacenar los datos
for row in table.find_all('tr')[1:]:  # Omitir el encabezado de la tabla
    cells = row.find_all('td')
    if len(cells) > 2:
        artist = cells[0].text.strip()
        song = cells[1].text.strip()
        weeks = cells[2].text.strip()
        # Insertar en la base de datos, ignorando duplicados
        c.execute(
            'INSERT OR IGNORE INTO songs (artist, song, weeks_at_number_one) VALUES (?, ?, ?)', (artist, song, weeks))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()
conn = sqlite3.connect('songs.db')
c = conn.cursor()

# Consultar la base de datos
c.execute('SELECT * FROM songs')

# Recuperar todos los registros
rows = c.fetchall()

# Imprimir los datos recuperados
for row in rows:
    print(row)

# Cerrar la conexión a la base de datos
conn.close()
