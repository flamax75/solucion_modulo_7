import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from geopy.geocoders import Nominatim


def extraer_datos_desde_url(url):
    try:
        # Realizar la solicitud GET a la URL
        response = requests.get(url)
        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            # Especificar la codificación como utf-8 al decodificar el contenido de la respuesta
            response.encoding = 'utf-8'
            # Parsear el contenido HTML de la respuesta
            soup = BeautifulSoup(response.text, 'html.parser')
            # Encontrar la tabla en la página
            tabla = soup.find('table', {'class': 'wikitable'})
            # Extraer los datos de la tabla
            html_str = str(tabla)
            # Utilizar StringIO para evitar la advertencia
            datos = pd.read_html(StringIO(html_str))[0]
            return datos
        else:
            print("Error al obtener el contenido de la URL:", response.status_code)
            return None
    except Exception as e:
        print("Error al extraer datos desde la URL:", e)
        return None


def obtener_codigo_pais(nombre_pais):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(nombre_pais)
    if location:
        return location.raw['display_name'].split(",")[-1].strip()
    else:
        return "Desconocido"


def limpiar_y_mostrar_datos(datos):
    try:
        # Limpiar valores dobles de año
        datos['Año'] = datos['Año'].apply(
            lambda x: x.split('/')[0] if '/' in x else x)
        # Limpiar valores múltiples de país y convertirlos en códigos
        datos['País'] = datos['País'].apply(lambda x: obtener_codigo_pais(x))
        print("Datos limpiados exitosamente:")
        print(datos)
    except Exception as e:
        print("Error al limpiar datos extraídos:", e)


def menu():
    url = "https://es.wikipedia.org/wiki/Anexo:Sencillos_número_uno_en_España#Canciones_con_más_semanas_en_el_número_uno"
    datos_extraidos = None  # Inicializar los datos extraídos como None

    while True:
        print("\nMENU:")
        print("1. Extraer datos desde la URL")
        print("2. Mostrar datos extraídos")
        print("3. Limpiar y mostrar datos")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if datos_extraidos is None:  # Verificar si los datos ya han sido extraídos
                datos_extraidos = extraer_datos_desde_url(url)
                if datos_extraidos is not None:
                    print("Datos extraídos exitosamente.")
            else:
                print("Los datos ya han sido extraídos. Evitando duplicados.")
        elif opcion == "2":
            if datos_extraidos is not None:
                print("Datos extraídos:")
                print(datos_extraidos)
            else:
                print(
                    "No hay datos para mostrar. Por favor, extraiga los datos primero.")
        elif opcion == "3":
            if datos_extraidos is not None:
                limpiar_y_mostrar_datos(datos_extraidos)
            else:
                print(
                    "No hay datos para limpiar. Por favor, extraiga los datos primero.")
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")


if __name__ == "__main__":
    menu()
