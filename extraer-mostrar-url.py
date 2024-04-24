import requests
from bs4 import BeautifulSoup


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

            # Agregar los datos a la lista
            canciones.append((cancion, interprete, año, semanas, pais))

        return canciones
    else:
        # Si la solicitud no fue exitosa, imprimir el código de estado
        print("Error al obtener la página. Código de estado:", response.status_code)
        return None


def mostrar_canciones(canciones):
    if canciones:
        for cancion, interprete, año, semanas, pais in canciones:
            print(
                f"Canción: {cancion} - interprete: {interprete}-año: {año} -semanas: {semanas} ,pais:-{pais}")
    else:
        print("No se han obtenido datos aún.")


# URL de la página que contiene la información de las canciones
url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'

while True:
    print("\nMENU:")
    print("1. Extraer datos de la página")
    print("2. Mostrar datos extraídos")
    print("3. Salir")

    opcion = input("Ingrese el número de la opción que desea: ")

    if opcion == "1":
        canciones_mas_semanas_numero_uno = obtener_canciones_mas_semanas_numero_uno(
            url)
        print("Datos extraídos exitosamente.")
    elif opcion == "2":
        mostrar_canciones(canciones_mas_semanas_numero_uno)
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")