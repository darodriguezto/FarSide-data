#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 08:25:21 2023

@author: daniel
"""
#PROGRAMA QUE PASA DEL ARCHIVO TXT CON LOS ETA A UN ARCHIVO CSV (TABLAS)

import csv
import re

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

    # Escribe la fila de encabezado
    escritor_csv.writerow(["strength", "date", "", "filename"])

    # Itera a través de las líneas del archivo de texto y escribe cada línea en el archivo CSV
    for linea in lineas:
        # Utiliza una expresión regular para dividir la línea en columnas
        datos = re.split(r'\s+', linea.strip())
        escritor_csv.writerow(datos)

print(f'El archivo "{nombre_archivo_txt}" se ha convertido a "{nombre_archivo_csv}" en formato CSV.')


'''
# Abre el archivo CSV en modo lectura
with open(nombre_archivo_csv, 'r', newline='') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    
    # Lee la fila de encabezado
    encabezado = next(lector_csv)
    
    # Cuenta el número de columnas en el encabezado
    num_columnas = len(encabezado)

print(f'El archivo CSV tiene {num_columnas} columnas.')
'''