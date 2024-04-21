def limpieza_años():
    conn = sqlite3.connect('canciones.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM canciones")
    filas = cursor.fetchall()

    for fila in filas:
        año_actual = fila[3]  # Obtener el valor actual del año
        if '/' in año_actual:  # Si hay múltiples años separados por "/"
            año_actual = año_actual.split('/')[0]  # Tomar el primer año
            cursor.execute(
                "UPDATE canciones SET año = ? WHERE cancion = ?", (año_actual, fila[0]))

    conn.commit()
    conn.close()

    print("Limpieza de años completada.")


# Llamar a la función limpieza_años para realizar la limpieza
limpieza_años()
