#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 12:08:30 2023

@author: daniel
"""

#PROGRAMA PARA AGRUPAR LOS DATOS DEL HISTOGRAMA DEL NEARSIDE Y LOS STRENGTH DEL FARSIDE (PROMEDIO) POR SEMANA

import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('2012.csv', sep='\t')
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
df.to_csv('2012_modificado.csv', index=False)



    