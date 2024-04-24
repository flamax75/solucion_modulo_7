import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import sqlite3

# Función para guardar los datos en la base de datos SQLite


def guardar_en_base_de_datos(canciones):
    # Conectar con la base de datos (se creará si no existe)
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()

    # Crear la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS canciones (
                        id INTEGER PRIMARY KEY,
                        cancion TEXT,
                        interprete TEXT,
                        año INTEGER,
                        semanas INTEGER,
                        pais TEXT
                    )''')

    # Insertar los datos en la tabla
    for cancion in canciones:
        try:
            cursor.execute(
                'INSERT INTO canciones VALUES (?, ?, ?, ?, ?, ?)', cancion)
        except sqlite3.IntegrityError:
            # Si hay un error de integridad (probablemente debido a un ID duplicado), ignora el registro
            continue

    # Guardar cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

    print("Datos guardados en la base de datos.")
# Función para ver los datos en la base de datos SQLite


def ver_en_base_de_datos():
    # Conectar con la base de datos
    conexion = sqlite3.connect('canciones.db')
    cursor = conexion.cursor()

    # Seleccionar todos los registros de la tabla
    cursor.execute('SELECT * FROM canciones')
    filas = cursor.fetchall()

    # Mostrar los datos en forma de tabla
    if filas:
        print("\nDatos en la base de datos:")
        print(tabulate(filas, headers=[
              "ID", "Canción", "Intérprete", "Año", "Semanas", "País"], tablefmt="grid"))
    else:
        print("La base de datos está vacía.")

    # Cerrar la conexión
    conexion.close()


# URL de la página que contiene la información de las canciones
# Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno
url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'


def obtener_canciones_mas_semanas_numero_uno(url):
    # Realizar la solicitud GET a la página
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar la tabla que contiene los datos
        tabla = soup.find('table', {'class': 'wikitable'})

        # Crear una lista para almacenar los datos
        canciones = []

        # Variable para llevar el conteo de registros
        id_registro = 1

        # Iterar sobre las filas de la tabla, excepto la primera (encabezados)
        for fila in tabla.find_all('tr')[1:]:
            # Obtener las celdas de la fila
            celdas = fila.find_all('td')

            # Extraer los datos de las celdas
            cancion = celdas[0].text.strip()
            interprete = celdas[1].text.strip()
            años_texto = celdas[2].text.strip()
            # Tomar solo el primer año del rango
            años = años_texto.split('/')[0]
            año = int(años)
            semanas = celdas[3].text.strip()
            pais = celdas[4].text.strip()

            # Agregar los datos a la lista con el ID automáticamente asignado
            canciones.append(
                (id_registro, cancion, interprete, año, semanas, pais))
            # Incrementar el contador de registros
            id_registro += 1

        return canciones
    else:
        # Si la solicitud no fue exitosa, imprimir el código de estado
        print("Error al obtener la página. Código de estado:", response.status_code)
        return None


def mostrar_canciones(canciones):
    if canciones:
        # Crear una lista de listas con los datos de las canciones
        datos_canciones = []
        for registro in canciones:
            id_registro, cancion, interprete, año, semanas, pais = registro
            datos_canciones.append(
                [id_registro, cancion, interprete, año, semanas, pais])

        # Generar la tabla usando tabulate
        tabla = tabulate(datos_canciones, headers=[
                         "ID", "Canción", "Intérprete", "Año", "Semanas", "País"], tablefmt="grid")
        print(tabla)
    else:
        print("No se han obtenido datos aún.")


# URL de la página que contiene la información de las canciones
url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'

while True:
    print("\nMENU:")
    print("1. Extraer datos de la página")
    print("2. Mostrar datos extraídos")
    print("3. Guardar en base de datos")
    print("4. Ver datos en base de datos")
    print("5. Salir")

    opcion = input("Ingrese el número de la opción que desea: ")

    if opcion == "1":
        canciones_mas_semanas_numero_uno = obtener_canciones_mas_semanas_numero_uno(
            url)
        print("Datos extraídos exitosamente.")
    elif opcion == "2":
        mostrar_canciones(canciones_mas_semanas_numero_uno)
    elif opcion == "3":
        if canciones_mas_semanas_numero_uno:
            guardar_en_base_de_datos(canciones_mas_semanas_numero_uno)
        else:
            print("No hay datos para guardar. Primero extrae los datos.")
    elif opcion == "4":
        ver_en_base_de_datos()
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")
