import pandas as pd
import json

# Leer el archivo JSON
with open("canciones.json", "r", encoding="utf-8") as json_file:
    datos_json = json.load(json_file)

# Convertir los datos en un DataFrame de Pandas
df = pd.DataFrame(datos_json)

# Mostrar el DataFrame
print(df)
