#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 21:07:48 2023

@author: daniel
"""

#PROGRAMA QUE ELIMINA LAS FRACCIONES DE DÍA EN LA TABLA 

import pandas as pd
import os
import argparse

def main(year):
    # Nombre del archivo CSV de entrada y salida
    carpeta_base = os.path.expanduser("~/Documentos/U/CarpetaPruebas")
    carpeta = os.path.join(carpeta_base, year)
    nombre_archivo_csv_entrada = os.path.expanduser(f"~/Documentos/GoSA/Far_Side/FarSide-data/Strength in Time/{year}/ETA.csv")
    nombre_archivo_csv_salida = os.path.join(carpeta, 'ETA_modified.csv')

    # Leer el archivo CSV
    df = pd.read_csv(nombre_archivo_csv_entrada)

    numfilas = len(df)
    for i in range(numfilas):
        print(df.iloc[i, 1])

    # Eliminar las fracciones de día en la segunda columna
    df.iloc[:, 1] = df.iloc[:, 1].str.split('.').str[0]

    # Guardar el DataFrame modificado en un nuevo archivo CSV
    df.to_csv(nombre_archivo_csv_salida, index=False)

    print(f'El archivo "{nombre_archivo_csv_entrada}" ha sido modificado y guardado como "{nombre_archivo_csv_salida}" en la carpeta de destino.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suprime las fracciones de día, es decir, deja entero el número de día")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder
    main(args.year)
