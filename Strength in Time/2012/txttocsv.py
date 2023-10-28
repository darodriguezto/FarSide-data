#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 08:25:21 2023

@author: daniel
"""

import csv

# Nombre del archivo de entrada y salida
nombre_archivo_txt = 'ETAlist.txt'
nombre_archivo_csv = 'ETA.csv'

# Abre el archivo de entrada en modo lectura
with open(nombre_archivo_txt, 'r') as archivo_txt:
    # Lee las líneas del archivo de texto
    lineas = archivo_txt.readlines()

# Abre el archivo de salida en modo escritura con la ayuda de la biblioteca CSV
with open(nombre_archivo_csv, 'w', newline='') as archivo_csv:
    # Crea un objeto escritor de CSV
    escritor_csv = csv.writer(archivo_csv)

    # Itera a través de las líneas del archivo de texto y escribe cada línea en el archivo CSV
    for linea in lineas:
        # Divide la línea en una lista de datos utilizando espacios como delimitador
        datos = linea.strip().split()  # Usa split() sin argumentos para dividir por espacios
        escritor_csv.writerow(datos)  # Escribe la lista de datos en el archivo CSV

print(f'El archivo "{nombre_archivo_txt}" se ha convertido a "{nombre_archivo_csv}" en formato CSV.')

