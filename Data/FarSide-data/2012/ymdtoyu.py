#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:21:00 2023

@author: daniel
"""

#PROGRAMA PARA PASAR DE FECHA A SEMANAS EN LA SEGUNDA COLUMNA

import csv
from datetime import datetime

# Nombre del archivo CSV de entrada y salida
nombre_archivo_csv_entrada = 'ETA_modified.csv'
nombre_archivo_csv_salida = 'ETA_modified_week.csv'

# Lista para almacenar filas modificadas
filas_modificadas = []

# Abrir el archivo CSV de entrada
with open(nombre_archivo_csv_entrada, 'r') as archivo_entrada:
    lector_csv = csv.reader(archivo_entrada)
    cabecera = next(lector_csv)  # Leer la cabecera

    # Añadir la cabecera al resultado
    filas_modificadas.append(cabecera)

    for fila in lector_csv:
        # Obtener la fecha de la segunda columna y convertirla a objeto datetime
        fecha = datetime.strptime(fila[1], '%Y-%m-%d')

        # Obtener el número de semana en formato 'Y-U'
        semana = fecha.strftime('%Y-%U')

        # Reemplazar la fecha original con el número de semana
        fila[1] = semana

        # Agregar la fila modificada a la lista
        filas_modificadas.append(fila)

# Guardar el resultado en un nuevo archivo CSV
with open(nombre_archivo_csv_salida, 'w', newline='') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida)
    escritor_csv.writerows(filas_modificadas)

print(f'El archivo "{nombre_archivo_csv_entrada}" ha sido modificado y guardado como "{nombre_archivo_csv_salida}".')
