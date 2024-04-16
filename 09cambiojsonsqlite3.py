import sqlite3
import json

# Leer el archivo JSON
with open("canciones.json", "r", encoding="utf-8") as json_file:
    datos_json = json.load(json_file)

# Establecer la conexión a la base de datos SQLite
conn = sqlite3.connect("canciones.db")

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Crear una tabla para almacenar las canciones si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS canciones (
                    Título TEXT,
                    Intérprete TEXT,
                    Año TEXT,
                    Semanas TEXT,
                    País TEXT
                )''')

# Insertar los datos en la tabla
for cancion in datos_json:
    cursor.execute("INSERT INTO canciones VALUES (?, ?, ?, ?, ?)",
                   (cancion["Título"], cancion["Intérprete"], cancion["Año"], cancion["Semanas"], cancion["País"]))

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Datos insertados en la base de datos SQLite.")
