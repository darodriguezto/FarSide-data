#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:21:00 2023

@author: daniel
"""

#PROGRAMA PARA PASAR DE FECHA A SEMANAS EN LA SEGUNDA COLUMNA

import csv
from datetime import datetime
import os
import argparse

def main(year):
# Nombre del archivo CSV de entrada y salida
    carpeta_base = os.path.expanduser("~/Documentos/GoSA/Far_Side/FarSide-data/correlation")
    carpeta = os.path.join(carpeta_base, year)
    nombre_archivo_csv_entrada = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/correlation/{year}/ETA_modified.csv")
    nombre_archivo_csv_salida = os.path.join(carpeta, 'ETA_modified_week.csv')
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convierte el forma año/mes/día a número de semana")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")
    
    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder
    main(args.year)