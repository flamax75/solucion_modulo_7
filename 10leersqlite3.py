import sqlite3

# Establecer la conexión a la base de datos SQLite
conn = sqlite3.connect("canciones.db")

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Consulta SQL para seleccionar todos los registros de la tabla
query = "SELECT * FROM canciones"

# Ejecutar la consulta
cursor.execute(query)

# Obtener todos los resultados de la consulta
registros = cursor.fetchall()

# Mostrar los resultados
for registro in registros:
    print(registro)

# Cerrar la conexión
conn.close()
