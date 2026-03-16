#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 01:21:11 2024

@author: daniel
"""

import pandas as pd
import os
import argparse


def main(year):
    carpeta_base = os.path.expanduser("~/Documentos/GoSA/Far_Side/FarSide-data/correlation")
    carpeta = os.path.join(carpeta_base, year)
    archivo_salida=os.path.join(carpeta,'tabla_datedetection.csv')
    # Cargar el archivo CSV en un DataFrame
    archivo_entrada=os.path.join(carpeta,"tabla_combinada_datedetection.csv")
    df = pd.read_csv(archivo_entrada)
    df.insert(4, value=0, column=None)
    
    # Obtener el número de filas en el DataFrame
    num_filas = len(df) 
    
    
    #PARA COMPROBAR SI LEE BIEN LAS COLUMNAS
    #for i in range(num_filas):
    #    print(df.iloc[i,4])
    
    
    
    # Recorrer las filas del DataFrame y realizar la comparación
    for i in range(num_filas):
        for j in range(num_filas):
            if df.iloc[j, 2] == df.iloc[i, 0]:
                df.iloc[i, 4] = df.iloc[j, 3]
                #print(df.iloc[i,0],' ',df.iloc[j,2],' ',df.iloc[i,4])
           # else:
           #     df.iloc[j, 4] = 0
                #print(df.iloc[i,0])
                # Eliminar la columna 3
    df = df.drop(df.columns[2], axis=1)
    
    # Pegar los datos de la columna 5 en lugar de la columna 3
    df[df.columns[2]] = df[df.columns[3]]
    
    column_to_drop = df.columns[2]
    df = df.drop(column_to_drop, axis=1)
    
    # Guardar el DataFrame modificado en un nuevo archivo CSV
    df.to_csv(archivo_salida , index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convierte archivo de texto a CSV.")
    parser.add_argument("year", type=str, help="Año de la carpeta que contiene el archivo de texto")
    parser.add_argument("--output_folder", type=str, default=".", help="Carpeta de destino para el archivo CSV")

    args = parser.parse_args()
    nombre_carpeta_destino = args.output_folder

    main(args.year)