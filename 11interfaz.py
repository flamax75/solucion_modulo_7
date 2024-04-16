import tkinter as tk
from tkinter import messagebox
import sqlite3
import json


def extraer_datos():
    # Aquí colocas tu código para extraer datos de la página web y guardarlos en un archivo JSON
    messagebox.showinfo(
        "Información", "Datos extraídos y guardados en canciones.json.")


def leer_archivo():
    # Aquí colocas tu código para leer los datos del archivo JSON y mostrarlos
    messagebox.showinfo("Información", "Datos leídos del archivo y mostrados.")


def insertar_bd():
    # Aquí colocas tu código para insertar los datos del archivo JSON en la base de datos SQLite
    messagebox.showinfo(
        "Información", "Datos insertados en la base de datos SQLite.")


def visualizar_bd():
    # Aquí colocas tu código para visualizar los datos de la base de datos SQLite
    messagebox.showinfo(
        "Información", "Datos de la base de datos visualizados.")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Usuario")

# Crear los botones
boton_extraer = tk.Button(ventana, text="Extraer Datos", command=extraer_datos)
boton_extraer.pack()

boton_leer = tk.Button(ventana, text="Leer Archivo", command=leer_archivo)
boton_leer.pack()

boton_insertar = tk.Button(ventana, text="Insertar en BD", command=insertar_bd)
boton_insertar.pack()

boton_visualizar = tk.Button(
    ventana, text="Visualizar BD", command=visualizar_bd)
boton_visualizar.pack()

# Iniciar el bucle de eventos
ventana.mainloop()
