import sqlite3
import pandas as pd

# Establecer la conexión a la base de datos SQLite
conn = sqlite3.connect("canciones.db")

# Consulta SQL para seleccionar todos los registros de la tabla de canciones
query = "SELECT * FROM canciones"

# Leer los datos de la base de datos en un DataFrame de Pandas
df = pd.read_sql_query(query, conn)

# Cerrar la conexión
conn.close()

# Mostrar el DataFrame
print(df)
