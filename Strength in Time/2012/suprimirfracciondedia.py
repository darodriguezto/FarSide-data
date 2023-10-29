#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 08:35:58 2023

@author: daniel
"""

#PROGRAMA QUE ELIMINA LAS FRACCIONES DE DÍA EN LA TABLA 

import pandas as pd

# Nombre del archivo CSV de entrada y salida
nombre_archivo_csv_entrada = 'ETA.csv'
nombre_archivo_csv_salida = 'ETA_modified.csv'


# Leer el archivo CSV
df = pd.read_csv(nombre_archivo_csv_entrada)

numfilas=len(df)
for i in range(numfilas):
    print(df.iloc[i,1])

# Eliminar las fracciones de día en la segunda columna
df.iloc[:, 1] = df.iloc[:, 1].str.split('.').str[0]

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv(nombre_archivo_csv_salida, index=False)

print(f'El archivo "{nombre_archivo_csv_entrada}" ha sido modificado y guardado como "{nombre_archivo_csv_salida}".')
